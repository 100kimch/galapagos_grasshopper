<template>
    <Page>
        <ActionBar title="Welcome to NativeScript-Vue!" android:flat="true"/>
        <TabView android:tabBackgroundColor="#53ba82"
                 android:tabTextColor="#c4ffdf"
                 android:selectedTabTextColor="#ffffff"
                 androidSelectedTabHighlightColor="#ffffff">
            <TabViewItem title="Tab 1">
                <FlexboxLayout flexWrap="wrap" alignItems="flex-start" backgroundColor="#3c495e">
                    <Label class="message" :text="msg" col="0" row="0"/>
                    <Button text="getPicture" @tap="getPicture" />
                    <Button text="onTakeShot" @tap="onTakeShot" />
                    <Placeholder @creatingView="onCreatingView" width="800" height="480" id="placeholder-view" />
                </FlexboxLayout>
            </TabViewItem>
            <TabViewItem title="Tab 2">
                <FlexboxLayout alignItems="flex-start" backgroundColor="#3c495e">
                    <!-- <Label class="message" :text="accelerometerSensor" col="0" row="0"/> -->
                    <Button text="sensor test" @tap="startUpdatingHeading" />
                    <Button text="sensor stop" @tap="stopUpdatingHeading" />
                    <Label class="message" :text="degree" />
                </FlexboxLayout>
            </TabViewItem>
            <TabViewItem title="Tab 3">
                <FlexboxLayout columns="*" rows="*" backgroundColor="#3c495e">
                    <!-- <Placeholder @creatingView="onCreatingView" id="placeholder-view" /> -->
                    <!-- <Label class="message" :text="degree" /> -->
                    <!-- <Label class="message" :text="gyroScope" col="0" row="0"/> -->
                    <!-- <HtmlView html="<h1>Hello!</h1><input type='file' accept='image/*' capture='camera' />" /> -->
                    <!-- <CameraPlus height="250" /> -->
                    <!-- <Placeholder creatingView="onCreatingView" id="placeholder-view"/> -->
                    <!-- <CameraPlus ref="CameraPlus" height="600" id="camPlus"
                        saveToGallery="true"      
                        showCaptureIcon="true"
                        showGalleryIcon="false"
                        showToggleIcon="false"       
                        showFlashIcon="false"
                        debug="true"
                        enableVideo="false"
                        confirmVideo="false"
                        defaultCamera="front" /> -->
                        <!-- @loaded="onCameraLoaded"
                        @photoCapturedEvent="photoCaptured($event)"
                        @errorEvent="onCameraError">     
                    </CameraPlus> -->
                </FlexboxLayout>
            </TabViewItem>
        </TabView>
    </Page>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import * as app from "tns-core-modules/application";
import { isAndroid, /*isIOS*/ } from "tns-core-modules/platform";
// import * as camera from "nativescript-camera";
// import { Image } from "tns-core-modules/ui/image";

import * as permissions from "nativescript-permissions";
import * as utils from "tns-core-modules/utils/utils";
// import * as platform from "tns-core-modules/platform/platform";

interface ConfigCam {
    mCameraId: any,
    mCaptureSession: android.hardware.camera2.CameraCaptureSession,
    mCameraDevice: android.hardware.camera2.CameraDevice,
    mStateCallBack: android.hardware.camera2.CameraDevice.StateCallback,
    mBackgroundHandler: any,
    mCameraOpenCloseLock: any,
    mTextureView: android.view.TextureView,
    mSurfaceTexture: android.graphics.SurfaceTexture,
    mPreviewRequestBuilder: android.hardware.camera2.CaptureRequest.Builder,
    mPreviewRequest: any,
    mImageReader: any,
    mCaptureCallback: any,
    mFlashSupported: any,
    mFile: any,
    mOnImageAvailableListener: android.media.ImageReader.OnImageAvailableListener,
    mSurfaceTextureListener: android.view.TextureView.SurfaceTextureListener
}

// // from Java : public static abstract class
// var newMyStateCallback = (android.hardware.camera2.CameraDevice.StateCallback as any).extend({
//     onOpened: function (cameraDevice) {
//         console.log("onOpened " + cameraDevice);

//         // mCameraOpenCloseLock.release();
//         // mCameraDevice = cameraDevice;
//         // createCameraPreviewSession();
//     },
//     onDisconnected: function (cameraDevice) {
//         console.log("onDisconnected");

//         // mCameraOpenCloseLock.release();
//         // cameraDevice.close();
//         // mCameraDevice = null;
//     },
//     onError: function (cameraDevice, error) {
//         console.log("onError");
//         console.log("onError: device = " + cameraDevice);
//         console.log("onError: error =  " + error);

//         // mCameraOpenCloseLock.release();
//         // cameraDevice.close();
//         // mCameraDevice = null;
//     },
//     onClosed: function (cameraDevice) {
//         console.log("onClosed");
//     }
// });

@Component
export default class App extends Vue {
    // private retries = 0;
    private msg = "Hello World!";
    private sensorUpdate;
    private sensorManager;
    private event;
    private _cam: ConfigCam = Object.freeze({
        mCameraId: null,
        mCaptureSession: null,
        mCameraDevice: null,
        mStateCallBack: null,
        mBackgroundHandler: null,
        mCameraOpenCloseLock: new java.util.concurrent.Semaphore(1),
        mTextureView: null,
        mSurfaceTexture: null,
        mPreviewRequestBuilder: null,
        mPreviewRequest: null,
        mImageReader: null,
        mCaptureCallback: null,
        mFlashSupported: null,
        mFile: null,
        mOnImageAvailableListener: new android.media.ImageReader.OnImageAvailableListener({
            onImageAvailable: (reader) => {
                console.log("onImageAvailable: ", reader);
            }
        }),
        mSurfaceTextureListener: new android.view.TextureView.SurfaceTextureListener({
            onSurfaceTextureAvailable: (texture, width, height) => {
                console.log("onSurfaceTextureAvailable()");
                this.cam.mSurfaceTexture = texture;
                this.createCameraPreviewSession();
            },

            onSurfaceTextureSizeChanged: (texture, width, height) => {
                console.log("onSurfaceTextureSizeChanged()");
                // configureTransform(width, height);
            },

            onSurfaceTextureDestroyed: (texture) => {
                // console.log("onSurfaceTextureDestroyed()");
                return true;
            },

            onSurfaceTextureUpdated: (texture) => {
                // console.log("onSurfaceTextureUpdated");
            }
        })
    });
    private cam: ConfigCam = Object.assign({}, this._cam);
    private state = Object.freeze({
        'STATE_PREVIEW': 0,
        'STATE_WAITING_LOCK': 1,
        'STATE_WAITING_PRECAPTURE': 2,
        'STATE_WAITING_NON_PRECAPTURE': 3,
        'STATE_PICTURE_TAKEN': 4
    });
    private mState = this.state['STATE_PREVIEW'];

    private MyStateCallback = (android.hardware.camera2.CameraDevice.StateCallback as any).extend({
        onOpened: (cameraDevice) => {
            console.log("onOpened(): ", cameraDevice);
            this.cam.mCameraOpenCloseLock.release();
            this.cam.mCameraDevice = cameraDevice;
            this.createCameraPreviewSession();
        },
        onDisconnected: (cameraDevice) => {
            console.log("onDisconnected()", cameraDevice);
            this.cam.mCameraOpenCloseLock.release();
            cameraDevice.close();
            this.cam.mCameraDevice = null;
        },
        onError: (cameraDevice, error) => {
            console.log("onError(): device = ", cameraDevice, "error = ", error);
            this.cam.mCameraOpenCloseLock.release();
            cameraDevice.close();
            this.cam.mCameraDevice = null;
        },
        onClosed: (cameraDevice) => {
            console.log("onClosed", cameraDevice);
        }
    });

    // private MyStateCallback = class nStateCallback extends java.lang.Object {
    //     // private cam = {
    //     //     mCameraOpenCloseLock: new java.util.concurrent.Semaphore(1),
    //     //     mCameraDevice: null,
    //     // }
    //     onOpened(cameraDevice) {
    //         console.log("onOpened(): ", cameraDevice);
    //         // this.cam.mCameraOpenCloseLock.release();
    //         // this.cam.mCameraDevice = cameraDevice;
    //         // this.createCameraPreviewSession();
    //     }
    //     onDisconnected(cameraDevice) {
    //         console.log("onDisconnected()", cameraDevice);
    //         // this.cam.mCameraOpenCloseLock.release();
    //         // cameraDevice.close();
    //         // this.cam.mCameraDevice = null;
    //     }
    //     onError(cameraDevice, error) {
    //         console.log("onError(): device = ", cameraDevice, "error = ", error);
    //         // this.cam.mCameraOpenCloseLock.release();
    //         // cameraDevice.close();
    //         // this.cam.mCameraDevice = null;
    //     }
    //     onClosed(cameraDevice) {
    //         console.log("onClosed", cameraDevice);
    //     }
    // };

    private MyCameraCaptureSessionStateCallback = (android.hardware.camera2.CameraCaptureSession.StateCallback as any).extend({
        onConfigured: (cameraCaptureSession) => {
            console.log("onConfigured(): ", cameraCaptureSession);

            if (this.cam.mCameraDevice === null) return;

            this.cam.mCaptureSession = cameraCaptureSession;
            this.cam.mPreviewRequest = this.cam.mPreviewRequestBuilder.build();
            this.cam.mCaptureSession.setRepeatingRequest(this.cam.mPreviewRequest, new this.MyCaptureSessionCaptureCallback(), null);
        },
        onConfigureFailed: (cameraCaptureSession) => {
            console.log("onConfigureFailed(): ", cameraCaptureSession);
        }
    });

    private MyCaptureSessionCaptureCallback = (android.hardware.camera2.CameraCaptureSession.CaptureCallback as any).extend({
        process: (result) => {
            switch(this.mState) {
                case this.state['STATE_PREVIEW']: {
                    break;
                }
                case this.state['STATE_WAITING_LOCK']: {
                    const afState = result.get(android.hardware.camera2.CaptureResult.CONTROL_AF_STATE);
                    if (afState === null) {
                        this.captureStillPicture();
                    } else if (android.hardware.camera2.CaptureResult.CONTROL_AF_STATE_FOCUSED_LOCKED === afState ||
                    android.hardware.camera2.CaptureResult.CONTROL_AF_STATE_NOT_FOCUSED_LOCKED === afState) {
                        const aeState = result.get(android.hardware.camera2.CaptureResult.CONTROL_AE_STATE);
                        if (aeState === null || 
                        aeState == android.hardware.camera2.CaptureResult.CONTROL_AE_STATE_CONVERGED) {
                            this.mState = this.state['STATE_PICTURE_TAKEN'];
                            this.captureStillPicture();
                        } else {
                            this.runPrecaptureSequence();
                        }
                    }
                    break;
                }
                case this.state['STATE_WAITING_PRECAPTURE']: {
                    const aeState = result.get(android.hardware.camera2.CaptureResult.CONTROL_AE_STATE);
                    if (aeState === null ||
                        aeState == android.hardware.camera2.CaptureResult.CONTROL_AE_STATE_PRECAPTURE ||
                        aeState == android.hardware.camera2.CaptureRequest.CONTROL_AE_STATE_FLASH_REQUIRED) {
                            this.mState = this.state['STATE_WAITING_NON_PRECAPTURE'];
                    }
                    break;
                }
                case this.state['STATE_WAITING_NON_PRECAPTURE']: {
                    const aeState = result.get(android.hardware.camera2.CaptureResult.CONTROL_AE_STATE);
                    if (aeState === null ||
                        aeState != android.hardware.camera2.CaptureResult.CONTROL_AE_STATE_PRECAPTURE) {
                        this.captureStillPicture();
                    }
                    break;
                }
            }
        },
        onCaptureProgressed(session, request, partialResult) {
            // console.log("onCaptureProgressed()");
            this.process(partialResult);
        },
        onCaptureCompleted(session, request, result) {
            // console.log("onCaptureCompleted()");
            this.process(result);
        },
        onCaptureFailed(session, request, failure) {
            console.log("onCaptureFailed(): ", failure);
        }
    });

    
    mounted() {
        // this.sensors.setListener(this.sensorListener);
        // this.getAccelerometer();
        setTimeout(() => {
            // console.log("camManager: ", app.android.context.getSystemService("camera"));
            // console.log("context: ", app.android.context);
            // this.onCreatingView();
        }, 2000);
        app.android.registerBroadcastReceiver(
            android.content.Intent.ACTION_SCREEN_OFF,
            () => {console.log("time ticked.")}
        );

        // console.log(app.android.context.CAMERA_SERVICE);
        // console.log(app.android.context.getSystemService(app.android.context.CAMERA_SERVICE));
    }

    get degree() {
        return this.event;
    }

    public onCreatingView(args) {
        if (app.android) {
            // if (!permissions.hasPermission(android.Manifest.permission.CAMERA)) {
            //     console.error("Application does not have permissions to camera");
            //     this.requestPermissions();
            //     this.retries += 1;
            //     if (this.retries < 5)
            //         setTimeout(() => {
            //             this.getPicture();
            //         }, 3000);
            //     else
            //         this.retries = 0;
            //     return;
            // }

            const context: typeof app.android.context = app.android.context;
            const cameraManager: android.hardware.camera2.CameraManager = context.getSystemService(android.content.Context.CAMERA_SERVICE);
            const cameras = JSON.parse(java.util.Arrays.toString(cameraManager.getCameraIdList()));
            console.log("onCreatingView():");
            console.log("cameras: ", java.util.Arrays.toString(cameras));
            console.log("cameraManager: ", String(cameraManager));
            console.log("permission: ", permissions.hasPermission(android.Manifest.permission.CAMERA));

            if (cameras.length == 0) {
                console.error("no cameras detected.");
                return;
            }

            for (let c in cameras) {
                // let cameraSpecs = java.util.Objects.toString(cameraManager.getCameraCharacteristics(String(cameras[c])));
                console.log("cameras[" + c + "]:", cameras[c]);
                const cameraSpecs = cameraManager.getCameraCharacteristics(String(cameras[c]));
                console.log("cameraSpecs: ", cameraSpecs);
                const facing = cameraSpecs.get(android.hardware.camera2.CameraCharacteristics.LENS_FACING);
                if (facing != null && facing == android.hardware.camera2.CameraCharacteristics.LENS_FACING_BACK)
                    this.cam.mCameraId = cameras[c];

                // NOTE: get available camera image size
                const map = cameraSpecs.get(android.hardware.camera2.CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
                const format = map.getOutputSizes(android.graphics.ImageFormat.JPEG);

                if (format) {
                    const dimensions = format[0].toString().split('x');
                    const largestWidth = +dimensions[0];
                    const largestHeight = +dimensions[1];

                    this.cam.mImageReader = new (android.media.ImageReader.newInstance as any)(largestWidth, largestHeight, android.graphics.ImageFormat.JPEG, /*maxImages*/ 2);

                    this.cam.mImageReader.setOnImageAvailableListener(this.cam.mOnImageAvailableListener, this.cam.mBackgroundHandler);
                }
            }

            console.log("final this.cam.mCameraId: ", this.cam.mCameraId);

            console.log("executing...", Object.getOwnPropertyNames(cameraManager));

            this.cam.mStateCallBack = new this.MyStateCallback();

            // let testing = new this.MyStateCallback();
            // cameraManager.openCamera(String(cameras[0]), testing, null);
            // console.log("executing done.")



            // NOTE: API 23 runtime permission check
            if (android.os.Build.VERSION.SDK_INT < android.os.Build.VERSION_CODES.LOLLIPOP || permissions.hasPermission(android.Manifest.permission.CAMERA))
                cameraManager.openCamera(String(this.cam.mCameraId), this.cam.mStateCallBack, this.cam.mBackgroundHandler);
            else
                permissions.requestPermissions([
                    android.Manifest.permission.WRITE_EXTERNAL_STORAGE,
                    android.Manifest.permission.CAMERA
                ]).then(() => 
                    cameraManager.openCamera(String(this.cam.mCameraId), this.cam.mStateCallBack, this.cam.mBackgroundHandler)
                ).catch((err) =>
                    alert("Could not get camera permission. msg: " + err)
                );
            
            this.cam.mTextureView = new android.view.TextureView(context);
            this.cam.mTextureView.setSurfaceTextureListener(this.cam.mSurfaceTextureListener);
            args.view = this.cam.mTextureView;

            // cameraManager.openCamera(this.cam.mCameraId, new android.hardware.camera2.CameraDevice.StateCallback.class());
            // cameraManager.openCamera(this.cam.mCameraId, ()=> {});

        }
    }

    public createCameraPreviewSession() {
        console.log("createCameraPreviewSession()");

        if (!this.cam.mSurfaceTexture || !this.cam.mCameraDevice) {
            console.log("this.cam.mSurfaceTexture: ", this.cam.mSurfaceTexture);
            console.log("this.cam.mCameraDevice: ", this.cam.mCameraDevice);
            return;
        }

        const texture = this.cam.mTextureView.getSurfaceTexture();
        texture.setDefaultBufferSize(800, 480);
        const surface = new android.view.Surface(texture);

        this.cam.mPreviewRequestBuilder = this.cam.mCameraDevice.createCaptureRequest(android.hardware.camera2.CameraDevice.TEMPLATE_PREVIEW);
        this.cam.mPreviewRequestBuilder.addTarget(surface);

        const surfaceList = new java.util.ArrayList();
        surfaceList.add(surface);
        this.cam.mCameraDevice.createCaptureSession(surfaceList, new this.MyCameraCaptureSessionStateCallback(), null);

        console.log("createCameraPreviewSession() done.");
    }

    public onTakeShot() {
        if (app.android) {
            console.log("onTakeShot");
            this.lockFocus();
        }
    }

    public lockFocus() {
        console.log("lockFocus()");
        this.mState = this.state['STATE_WAITING_LOCK'];
        this.cam.mCaptureSession.capture(this.cam.mPreviewRequestBuilder.build(), this.cam.mCaptureCallback, this.cam.mBackgroundHandler);
    }

    public runPrecaptureSequence() {
        this.cam.mPreviewRequestBuilder.set(android.hardware.camera2.CaptureRequest.CONTROL_AE_PRECAPTURE_TRIGGER, android.hardware.camera2.CaptureRequest.CONTROL_AE_PRECAPTURE_TRIGGER_START);
        this.mState = this.state['STATE_WAITING_PRECAPTURE'];
        this.cam.mCaptureSession.capture(this.cam.mPreviewRequestBuilder.build(), this.cam.mCaptureCallback, this.cam.mBackgroundHandler);
    }

    public captureStillPicture() {
        const captureBuilder = this.cam.mCameraDevice.createCaptureRequest(android.hardware.camera2.CameraDevice.TEMPLATE_STILL_CAPTURE);
        captureBuilder.addTarget(this.cam.mImageReader.getSurface());

        // this.setAutoFlash(captureBuilder);

        const CaptureCallback = (android.hardware.camera2.CameraCaptureSession.CaptureCallback as any).extend({
            onCaptureCompleted: (session, request, result) => {
                console.log("onCaptureCompleted");

            }
        });

        this.cam.mCaptureSession.stopRepeating();
        this.cam.mCaptureSession.abortCaptures();
        this.cam.mCaptureSession.capture(captureBuilder.build(), new CaptureCallback(), null);
    }

    public receiverCallback(context, intent) {
        console.log("context: ", context);
        console.log("intent: ", intent);
    }

    public getPicture() {
        // console.log("getting pictures...");
        // if (!permissions.hasPermission(android.Manifest.permission.CAMERA)) {
        //     console.error("Application does not have permissions to camera");
        //     this.requestPermissions();
        //     this.retries += 1;
        //     if (this.retries < 5)
        //         setTimeout(() => {
        //             this.getPicture();
        //         }, 3000);
        //     return;
        // }
        // let density = utils.layout.getDisplayDensity();

        // let takePictureIntent = new android.content.Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        // let dateStamp = this.createDateTimeStamp();

        // console.log(density, takePictureIntent, dateStamp);

        // // let sdkVersionInt = parseInt(platform.device.sdkVersion);

        // // console.log("hw: ", JSON.stringify(android.hardware.camera2));
        // // android.hardware
        // // let cameraManager = android.hardware.camera2.CameraManager.getSystemService(app.android.context.CAMERA_SERVICE);
        // // let cameraManager = app.android.context.getSystemService(android.content.Context.CAMERA_SERVICE);
        // // let cameraManager = app.android.context.getSystemService(app.android.context.CAMERA_SERVICE);
        // // let cameraManager = app.android.foregroundActivity.getSystemService(app.android.context.CAMERA_SERVICE);
        // let cameraManager = app.android.context.getSystemService("camera");

        // // console.log("number of cameras: ", cameraIdList.length);
        // // console.log("context on getPicture(): ", context_sample);
        // console.log("cameraManager: ", cameraManager);

        // // let cameraIdList = JSON.parse(java.util.List(cameraManager.getCameraIdList()));
        // let cameraIdList = JSON.parse(java.util.Arrays.toString(cameraManager.getCameraIdList()));
        // // let path = cameraIdList.listFiles();
        // // let facingList = [];

        // console.log("Camera Id List: ", cameraIdList);
        // // console.log("Camera Id path: ", path);

        // if (cameraIdList.length == 0) {
        //     console.error("no cameras detected.");
        //     return;
        // }

        // let possibleCandidate;
        // for (let c in cameraIdList) {
        //     // let characteristics = java.util.Objects.toString(cameraManager.getCameraCharacteristics(String(cameraIdList[c])));
        //     let characteristics = cameraManager.getCameraCharacteristics(String(cameraIdList[c]));
        //     let facing = characteristics.get(android.hardware.camera2.CameraCharacteristics.LENS_FACING);
        //     if  (facing != null && facing == android.hardware.camera2.CameraCharacteristics.LENS_FACING_FRONT)
        //         possibleCandidate = cameraIdList[c];
        //     // facingList.push(characteristics.LENS_FACING);
        // }
        // // cameraManager.openCamera(possibleCandidate, new android.hardware.camera2.CameraDevice.StateCallback.class());
        // // cameraManager.openCamera(possibleCandidate, ()=> {});

        // console.log("possibleCandidate: ", possibleCandidate);

        // // let MyStateCallback = android.hardware.camera2.CameraDevice.StateCallback.extend({
        // //     onOpened(cameraDevice) {
        // //         console.log("onOpened: " + cameraDevice);
        // //         // this.cam
                
        // //     }
        // // })

        // // this.cam.mStateCallBack = android.h
        // // console.log("MyStateCallback", MyStateCallback);

        // // let stateCallback = new MyStateCallback();

        // // StateCallback() {
        // //     public onOpened(param0: android.hardware.camera2.CameraDevice): void;
            
        // // });
        // //  (cameraDevice) => {
        // //     console.log("cameraDevice: ", cameraDevice);
        // // })
        // // console.log("facingList: ", facingList);

        // // app.android.foregroundActivity.startActivityForResult(takePictureIntent, 3453);
    }

    // public requestPermissions() {
    //     return permissions.requestPermissions([
    //         android.Manifest.permission.WRITE_EXTERNAL_STORAGE,
    //         android.Manifest.permission.CAMERA
    //     ]);
    // }

    public cameraActivity() {
            
    }

    public createDateTimeStamp() {
        let result = "";
        let date = new Date();

        result = date.getFullYear().toString() +
            ((date.getMonth() + 1) < 10 ? "0" + (date.getMonth() + 1).toString() : (date.getMonth() + 1).toString()) + (date.getDate() < 10 ? "0" + date.getDate().toString() : date.getDate().toString()) + "_" + date.getHours().toString() +
            date.getMinutes().toString() +
            date.getSeconds().toString();

        return result;
    }

    public onCameraLoaded(result) {
        this.cam = result.object;
        console.log("Camera loaded...");
    }

    // public onButtonCapture() {
    //     console.log('Take Picture');
    //     this.image = this.cam.takePicture({ saveToGallery: true });     
    // }

    public photoCaptured(args){
        console.log("ARGS - ", args)
    }

    public takePicture() {
        // camera.requestPermissions().then(() => {
        // this.msg = "Done permissioning";
        // setTimeout(() => {
        //     camera.takePicture().then(imageAsset => {
        //         console.log("Result is an image asset instance");
        //         this.msg = "Done taking picture";
        //         var image = new Image();
        //         image.src = imageAsset;
        //     }).catch(err => {
        //         console.log("Error: ", err.message);
        //         this.msg = "Error on taking picture";
        //     })
        // }, 5000);
        
        // });
    }

    public startUpdatingHeading() {
        if (this.sensorUpdate || this.sensorUpdate) {
            return;
        }
        if (isAndroid) {
            this.sensorManager = app.android.foregroundActivity.getSystemService(
                android.content.Context.SENSOR_SERVICE
            );

            this.sensorUpdate = new android.hardware.SensorEventListener({
                onAccuracyChanged: (sensor: any, accuracy: any) => {
                    console.log(accuracy, sensor)
                },
                onSensorChanged: (event: any) => {
                    // Here is the result we need for Android platform
                    // console.log(event.values[0]);
                    console.log(event.values[0], event.values[1], event.values[2]);
                    this.event = event;
                }
            });

            const orientationSensor = this.sensorManager.getDefaultSensor(android.hardware.Sensor.TYPE_ROTATION_VECTOR);
            // const orientationSensor = this.sensorManager.         getDefaultSensor(android.hardware.Sensor.TYPE_ORIENTATION);
            
            this.sensorManager.registerListener(
                this.sensorUpdate,
                orientationSensor,
                android.hardware.SensorManager.SENSOR_DELAY_UI
            );
        }
    }

    public stopUpdatingHeading() {
        if (!this.sensorManager || !this.sensorUpdate) {
        return;
        }

        if (isAndroid) {
        this.sensorManager.unregisterListener(this.sensorUpdate);
        }

        this.sensorManager = null;
        this.sensorUpdate = null;
    }

    public getAccelerometer() {
        // this.accelerometerSensor = this.sensors.startSensor(android.hardware.Sensor.TYPE_LINEAR_ACCELERATION, SensorDelay.FASTEST);

        // // here we are using the android const 4 which is for the TYPE_GYROSCOPE sensor
        // // https://developer.android.com/reference/android/hardware/Sensor.html#TYPE_GYROSCOPE
        // // we are passing the third argument to `startSensor` which is for maxReportLatency, if the sensor is able to support FIFO this will register the sensor with the reporting latency value, if not, the sensor registers on the background thread as normal
        // this.gyroScope =  this.sensors.startSensor(4, SensorDelay.NORMAL, 4000000);

        // // maybe you wanna use a timeout and stop it after 8 seconds
        // setTimeout(() => {
        //     this.sensors.stopSensor(this.gyroScope);
        // }, 8000)
    }
}
</script>

<style scoped>
    ActionBar {
        background-color: #53ba82;
        color: #ffffff;
    }

    .message {
        vertical-align: center;
        text-align: center;
        font-size: 20;
        color: #333333;
    }
</style>
