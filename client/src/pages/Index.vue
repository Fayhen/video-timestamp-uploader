<template>
  <q-page class="flex column q-pa-xl">
    <q-form @submit.prevent="sendVideo()">

      <span class="inline-block text-bold q-mb-md">{{ helperMessage }}</span>

      <q-file
        v-model="videoFile"
        filled
        clearable
        label="Click here to select a video file."
        accept=".webm, video/*"
        @update:model-value="getVideoData()"
      />

      <div class="q-mt-xl">

        <p v-if="!!videoFile === false">No video file selected.</p>

        <div v-else class="column content-center">

          <div class="text-left full-width">
            <p>
              Your video has a duration of <strong>{{ parsedDuration }}</strong> ({{ Math.floor(fullDuration) }} seconds).
              Please set desired timestamps for the beggining and end of audio transcription in the fields below.
            </p>
            <div class="row full-width">

              <q-input
                fill-mask
                bottom-slots
                v-model="timestampStart"
                :error="invalidTimestampStart"
                lazy-rules="ondemand"
                mask="fulltime"
                label="Start"
                class="col-grow"
              >
                <template v-slot:error>
                  Initial time can't be higher than the video duration.
                </template>
              </q-input>

              <q-input
                fill-mask
                bottom-slots
                v-model="timestampEnd"
                :error="invalidTimestampEnd"
                lazy-rules="ondemand"
                mask="fulltime"
                label="End"
                class="col-grow"
              >
                <template v-slot:error>
                  End time can't be higher than video duration or lower than initial time.
                </template>
              </q-input>

            </div>
          </div> 

        </div>

      </div>

      <q-btn
        type="submit"
        label="Submit"
        color="primary"
        class="q-mt-md"
        :disabled="!!videoFile === false"
      />

      <q-btn
        label="Show video"
        class="q-mt-md q-ml-md"
        :disabled="!!videoFile === false || !!filePreview === false"
        @click="showPlayer = !showPlayer"
      />

      <q-dialog seamless v-model="showPlayer">
        <div class="column content-center bg-black">
          <video controls width="500" :src="filePreview">
            Sorry, your browser doesn't support embedded videos.
          </video>
          <q-btn square color="dark" label="Close" v-close-popup />
        </div>
      </q-dialog>

      <!-- <q-btn
        label="Log video data to console"
        class="q-mt-md q-ml-md"
        @click="logVideoData()"
      /> -->
    </q-form>

    <!-- <div v-if="videoFile && filePreview" class="column content-center q-mt-md">
      <div>
        <p>Current duration: {{ fullDuration }}</p>
      </div>
      <video controls width="500" :src="filePreview">
        Sorry, your browser doesn't support embedded videos.
      </video>
    </div> -->

    <q-input
      readonly
      v-model="transcription"
      :loading="waitingTranscription"
      type="textarea" 
      class="q-mt-xl"
    />
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'PageIndex',

  data () {
    return {
      videoFile: null,
      filePreview: null,
      fullDuration: 0,
      parsedDuration: 0,
      timestampStart: '',
      timestampEnd: '',
      invalidTimestampStart: false,
      invalidTimestampEnd: false,
      waitingTranscription: false,
      transcription: 'Your transcription will appear here.',
      helperMessage: 'Please select a video file to continue.',
      showPlayer: false
    }
  },

  computed: {
    parsedTimestampStart: function () {
      if (this.timestampStart) {
        const [hours, minutes, seconds] = this.timestampStart.split(':')
        return (+hours * 60 * 60) + (+minutes * 60) + (+seconds)
      } else {
        return 0
      }
    },

    parsedTimestampEnd: function () {
      if (this.timestampEnd) {
        const [hours, minutes, seconds] = this.timestampEnd.split(':')
        return (+hours * 60 * 60) + (+minutes * 60) + (+seconds)
      } else {
        return 0
      }
    }
  },

  methods: {
    /**
     * This function will load the video file into memory in order
     * to retrieve its duration from metadata. The loaded video is
     * alse stored in the 'filePreview' variable, which is used to
     * display the video in the page.
     * 
     * A return value of 0 means there was no video file to load, such
     * as upon clearing the form prior to selecting a new video.
     */
    loadVideoData () {
      return new Promise ((resolve, reject) => {
        try {
          // Clear memory if needed
          if (!!this.filePreview === true) {
            URL.revokeObjectURL(this.filePreview)
          }
          this.filePreview = null

          // Create new URL object with video file
          if (!!this.videoFile === true) {
            this.filePreview = URL.createObjectURL(this.videoFile)

            // Asign URL to HTML video element and use metadata to get duration
            const videoElement = document.createElement('video')
            videoElement.src = this.filePreview

            videoElement.onloadedmetadata = function () {
              resolve(this.duration)
            }
          
          // Return '0' if no video file was found
          } else {
            this.filePreview = null

            resolve(0)
          }
        } catch (error) {
          this.filePreview = null
          reject(error)
        }
      })
    },

    /**
     * This function handles both calling the video loader function
     * and setting related form variables.
     */
    async getVideoData () {
      // Set back default values to variables
      this.fullDuration = 0
      this.parsedDuration = 0
      this.timestampStart = ''
      this.timestampEnd = ''
      this.invalidTimestampStart = false
      this.invalidTimestampEnd = false
      this.transcription = 'Your transcription will appear here.'

      try {
        // Load video into memory and retrieve its duration (s)
        const duration = await this.loadVideoData()
        
        // Parse duration string and set helper message for next step
        if (duration > 0) {
          this.fullDuration = duration
          this.parsedDuration = new Date(duration * 1000)
            .toISOString()
            .substr(11, 8)
          this.helperMessage = 'Please select a start and end time for audio transcription in the fields below.'
        
        // A duration of zero means there is no file to read (ex.: cleared the form)
        } else {
          this.fullDuration = 0
          this.parsedDuration = 0
          this.timestampStart = ''
          this.timestampEnd = ''
          this.helperMessage = 'Please select a video file to continue.'
        }
      } catch (error) {
        // Set back default values and notify user if error occurs
        this.fullDuration = 0
        this.parsedDuration = 0
        this.timestampStart = ''
        this.timestampEnd = ''
        this.helperMessage = 'Please select a video file to continue.'

        console.log(error)
        this.$q.notify({
          type: 'negative',
          message: 'An error ocurred while loading the video.'
        })
      }
    },

    /**
     * Logs video file data to the console.
     */
    logVideoData () {
      if (!!this.videoFile === false) {
        console.log("No video file selected.")
      } else {
        console.log(this.videoFile)
        console.log(this.timestampStart)
        console.log(this.timestampEnd)
        console.log(this.parsedTimestampStart)
        console.log(this.parsedTimestampEnd)
      }
    },

    /**
     * Custom validator for the inputted start time. It ensures
     * the value does not exceed the video duration.
     */
    validateTimestapStart () {
      this.invalidTimestampStart = this.parsedTimestampStart >= this.fullDuration
    },
    
    /**
     * Custom validator for the inputted end time. It ensures
     * the value does not exceed the video duration, and also
     * that it is higher than the start time.
     */
    validateTimestapsEnd () {
      this.invalidTimestampEnd = this.parsedTimestampEnd >= this.fullDuration
        || this.parsedTimestampEnd < this.parsedTimestampStart
        || !!this.parsedTimestampEnd === false
    },

    /**
     * Form submission method. Calls for custom form validation
     * prior to sending data.
     */
    async sendVideo () {
      // Timestamps validation
      this.validateTimestapStart()
      this.validateTimestapsEnd()

      // Notify user of any problems
      if (this.invalidTimestampStart || this.invalidTimestampEnd || this.videoFile === null) {
        this.$q.notify({
          type: 'negative',
          message: 'Unable to submit. Please review your inputted timestamps.'
        })
      } else {
        // Proceed with data submission if no errors found
        const formData = new FormData()
        formData.append('videoFile', this.videoFile)
        formData.append('startTime', this.parsedTimestampStart)
        formData.append('endTime', this.parsedTimestampEnd)
        this.waitingTranscription = true
        
        try {
          this.helperMessage = 'Your video is being submitted...'
          const response = await this.$axios({
            method: 'post',
            url: 'http://127.0.0.1:5000/video',
            data: formData,
            headers: { 'content-type': 'multipart/form-data' }
          })

          // Get the transcription from the response
          const { data } = response
          const transcription = data.transcription
          this.transcription = transcription
          this.waitingTranscription = false
          this.helperMessage = 'Video transcription received and available below.'
        } catch (error) {
          this.waitingTranscription = false
          this.transcription = 'Your transcription will appear here.',
          this.helperMessage = 'An error occurred while processing the transcription. Try clearing the form and resubmitting the data.'
          console.error(error)
        }
      }
    }
  }
})
</script>
