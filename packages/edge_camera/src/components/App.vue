<template>
    <Page>
        <ActionBar title="Welcome to NativeScript-Vue!" android:flat="true"/>
        <TabView android:tabBackgroundColor="#53ba82"
                 android:tabTextColor="#c4ffdf"
                 android:selectedTabTextColor="#ffffff"
                 androidSelectedTabHighlightColor="#ffffff">
            <TabViewItem title="Tab 1">
                <FlexboxLayout alignItems="flex-start" backgroundColor="#3c495e">
                    <Label class="message" :text="msg" col="0" row="0"/>
                    <Button text="getPicture" @tap="getPicture" />
                    <Button text="sensor test" @tap="takePicture" />
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
                <FlexboxLayout columns="*" rows="*">
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
import * as app from "tns-core-modules/application";
import { isAndroid, isIOS } from "tns-core-modules/platform";
import * as camera from "nativescript-camera";
import { Image } from "tns-core-modules/ui/image";

export default {
    data() {
        return {
            msg: 'Hello World!',
            sensorUpdate: null,
            sensorManager: null,
            event: null,
            captures: [],
            imgReport: [],
            frontCam: false,
            webcam: null,
            img: null,
            camera: null,
            deviceId: null,
            devices: [],
            cam: null
            //   googleKey: config.googleVisionKey
        }
    },
    mounted() {
        // this.sensors.setListener(this.sensorListener);
        // this.getAccelerometer();
    },
    computed: {
        degree() {
            return this.event;
        }
    },
    methods: {
        getPicture() {
        },
        onCameraLoaded(result) {
            this.cam = result.object;
            console.log("Camera loaded...");
        },

        onButtonCapture() {
            console.log('Take Picture');
            this.image = this.cam.takePicture({ saveToGallery: true });     
        },

        photoCaptured(args){
            console.log("ARGS - ", args)
        },

        takePicture() {
            camera.requestPermissions().then(() => {
            this.msg = "Done permissioning";
            setTimeout(() => {
                camera.takePicture().then(imageAsset => {
                    console.log("Result is an image asset instance");
                    this.msg = "Done taking picture";
                    var image = new Image();
                    image.src = imageAsset;
                }).catch(err => {
                    console.log("Error: ", err.message);
                    this.msg = "Error on taking picture";
                })
            }, 5000);
            
            });
        },
        startUpdatingHeading() {
            if (this.sensorUpdate || this.sensorUpdate) {
                return;
            }
            if (isAndroid) {
                this.sensorManager = app.android.foregroundActivity.getSystemService(
                    android.content.Context.SENSOR_SERVICE
                );

                this.sensorUpdate = new android.hardware.SensorEventListener({
                    onAccuracyChanged: (sensor: any, accuracy: any) => {
                    // console.log(accuracy)
                    },
                    onSensorChanged: (event: any) => {
                        // Here is the result we need for Android platform
                        // console.log(event.values[0]);
                        console.log(event.values[0], event.values[1], event.values[2]);
                        this.event = event;
                    }
                });

                const orientationSensor = this.sensorManager.         getDefaultSensor(android.hardware.Sensor.TYPE_ROTATION_VECTOR);
                // const orientationSensor = this.sensorManager.         getDefaultSensor(android.hardware.Sensor.TYPE_ORIENTATION);
                
                this.sensorManager.registerListener(
                    this.sensorUpdate,
                    orientationSensor,
                    android.hardware.SensorManager.SENSOR_DELAY_UI
                );
            }
        },
        stopUpdatingHeading() {
            if (!this.sensorManager || !this.sensorUpdate) {
            return;
            }

            if (isAndroid) {
            this.sensorManager.unregisterListener(this.sensorUpdate);
            }

            this.sensorManager = null;
            this.sensorUpdate = null;
        },
        getAccelerometer() {
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
