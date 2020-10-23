<template>
    <Page>
        <ActionBar title="Welcome to NativeScript-Vue!" android:flat="true"/>
        <TabView android:tabBackgroundColor="#53ba82"
                 android:tabTextColor="#c4ffdf"
                 android:selectedTabTextColor="#ffffff"
                 androidSelectedTabHighlightColor="#ffffff">
            <TabViewItem title="Tab 1">
                <GridLayout columns="*" rows="*">
                    <Label class="message" :text="msg" col="0" row="0"/>
                    <Button text="Choose Picture" @tap="selectPicture" />
                    <WrapLayout>
                        <Image v-for="img in images" :key="img.key" :src="img.src" width="75" height="75" />
                    </WrapLayout>
                </GridLayout>
            </TabViewItem>
            <TabViewItem title="Tab 2">
                <GridLayout columns="*" rows="*">
                    <Label class="message" text="Tab 2 Content" col="0" row="0"/>
                    <Button text="Take Picture" @tap="takePicture" />
                </GridLayout>
            </TabViewItem>
            <TabViewItem title="Tab 3">
                <GridLayout columns="*" rows="*">
                    <text>Accelerometer:</text>
                    <text>{{acceletometerData.x}}</text>
                    <text>{{acceletometerData}}</text>
                    <!-- <Label class="message" text="Tab 3 Content" col="0" row="0"/> -->
                    <!-- <WebRTCView #remoteVideoView height="50%" />
                    <WebRTCView #localVideoView height="30%" /> -->
                </GridLayout>
            </TabViewItem>
        </TabView>
    </Page>
</template>

<script lang="ts">
import * as camera from "nativescript-camera";
import * as imagepicker from "nativescript-imagepicker";
// import { WebRTC } from 'nativescript-webrtc-plugin';
// import { Image } from "tns-core-modules/ui/image";
import { Accelerometer } from "expo-sensors";

export default {
    data() {
        return {
            msg: 'Hello World!',
            images: [],
            accelerometerData: {}
        }
    },
    mounted() {
        // WebRTC.init();
        Accelerometer.addListener(accelerometerData => {
            this.accelerometerData = accelerometerData;
        });
        Accelerometer.setUpdateInterval(1000);
    },
    methods: {
        selectPicture() {
            let context = imagepicker.create({
                mode: 'multiple'
            });

            // context.authorize()
            //     .then(function() {
            //         return context.present();
            //     })
            //     .then(selection => {
            //         selection.forEach(selected => {
            //             console.log(JSON.stringify(selected));

            //             let img = new Image();
            //             img.src = selected;
            //             this.images.push(img);
            //         });
            //     }).catch(function (e) {
            //         console.log('error in selectPicture', e);
            //     });
        },
        takePicture() {
            // camera.requestPermissions()
            //     .then(() => {
            //         camera.takePicture({ width: 300, height: 300, keepAspectRatio: false, saveToGallery: true})
            //             .then(imageAsset => {
            //                 let img = new Image();
            //                 img.src = imageAsset;
            //                 this.images.push(img);
            //                 console.log('got ' + this.images.length + ' images now.')
            //             }).catch(e => {
            //                 console.log('error: ', e);
            //             })
            //     }).catch(e => {
            //         console.log('Error requesting permission');
            //     })
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
