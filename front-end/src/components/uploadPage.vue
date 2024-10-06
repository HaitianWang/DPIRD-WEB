<!--
This is the main content component of the DPIRD AgriVision application.
It guides users on how to upload TIF images, tracks the progress of AI predictions, displays input and output images, and provides detailed analysis of the predictions.
Users can upload ZIP files containing multi-spectral images, which are processed to detect crops, weeds, and other elements.
The interface also provides suggestions for weed removal based on the AI analysis, and users can navigate through the images or re-upload new images for analysis.
-->

<template>
  <div id="Content" style="display: flex; flex-direction: column; align-items: center;">
    <!-- How to Use Section: Guides users on how to upload images and what the colors in the output mean -->
    <el-card class="how-to-use" style="margin-bottom: 20px; width: 100%;">
      <div slot="header">
        <h3>How to Use</h3>
      </div>
      <p>Upload a zip file containing TIF image documents with different spectrums: Blue, Green, Red, RedEdge, NIR, RGB </p>
      <p>
        In the output image,
        <span style="color: lightgreen;">green</span> is crops,
        <span style="color: pink;">pink</span> is weed,
        <span style="color: lightgray;">white</span> is others.
      </p>
    </el-card>

    <!-- Progress Dialog: Indicates when AI is processing the prediction -->
    <el-dialog title="AI Prediction in Progress" :visible.sync="dialogTableVisible" :show-close="false"
               :close-on-press-escape="false" :append-to-body="true" :close-on-click-modal="false" :center="true">
      <el-progress :percentage="percentage"></el-progress>
      <span slot="footer" class="dialog-footer">Please wait patiently for about 3 seconds</span>
    </el-dialog>

    <!-- CT Images Section: Displays uploaded image and the AI-predicted result -->
    <div id="CT" style="width: 100%; margin-bottom: 20px;">
      <el-card id="CT_image_1" class="box-card" style="border-radius: 8px; width: 100%; margin-bottom: 20px;">
        <div class="demo-image__preview1">
          <!-- Loading and displaying the uploaded image -->
          <div v-loading="loading" element-loading-text="Uploading Image" element-loading-spinner="el-icon-loading">
            <el-image :src="currentImageUrl" class="image_1" :preview-src-list="allImageUrls"
                      style="border-radius: 3px 3px 0 0">
              <div slot="error">
                <div slot="placeholder" class="error">
                  <!-- Button to upload a zip file containing images -->
                  <el-button v-show="showbutton" type="primary" icon="el-icon-upload" class="download_bt"
                             v-on:click="true_upload">
                    Upload Zip
                    <input ref="upload" style="display: none" name="file" type="file" accept=".zip"
                           @change="update" />
                  </el-button>
                </div>
              </div>
            </el-image>
          </div>
          <div class="img_info_1" style="border-radius: 0 0 5px 5px">
            <span style="color: white">Multi-Spectrum Image</span>
          </div>
        </div>
        <div class="demo-image__preview2">
          <!-- Displaying the prediction result image -->
          <div v-loading="loading" element-loading-text="Processing, please wait"
               element-loading-spinner="el-icon-loading">
            <el-image :src="url_2" class="image_1" :preview-src-list="srcList1" style="border-radius: 3px 3px 0 0">
              <div slot="error">
                <div slot="placeholder" class="error">{{ wait_return }}</div>
              </div>
            </el-image>
          </div>
          <div class="img_info_1" style="border-radius: 0 0 5px 5px">
            <span style="color: white">Detection Result</span>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Analysis Section: Displays information based on the AI prediction -->
    <div id="info_weed" style="width: 100%;">
      <el-card style="border-radius: 8px">
        <div slot="header" class="clearfix">
          <span>Analysis</span>
          <!-- Button to upload a new image for analysis -->
          <el-button style="margin-left: 35px" v-show="!showbutton" type="primary" icon="el-icon-upload"
                     class="download_bt" v-on:click="true_upload2">
            Re-select Image
            <input ref="upload2" style="display: none" name="file" type="file" @change="update" />
          </el-button>
        </div>
        <!-- Tab to show AI prediction data -->
        <el-tabs v-model="activeName">
          <el-tab-pane label="Information" name="first">
            <el-table :data="feature_list" height="250" border style="width: 100%; text-align: center"
                      v-loading="loading" element-loading-text="Data is being processed, please wait"
                      element-loading-spinner="el-icon-loading" lazy>
              <el-table-column label="Key">
                <template slot-scope="scope">
                  <span>{{ scope.row[0] }}</span>
                </template>
              </el-table-column>
              <el-table-column label="Value">
                <template slot-scope="scope">
                  <span>{{ scope.row[1] }}</span>
                </template>
              </el-table-column>
              <!-- Display "No data" when there's no data -->
              <template slot="empty">
                <div class="no-data">No data</div>
              </template>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>

    <!-- Weed Removal Suggestions Section: Provides suggestions for weed removal -->
    <div id="info_weed2" style="width: 100%;">
      <el-card style="border-radius: 8px; margin-bottom: 20px;">
        <div slot="header" class="clearfix">
          <span>Weed Removal Suggestions</span>
        </div>
        <!-- Display weed removal suggestions or a fallback message if no suggestions are available -->
        <p v-if="filteredWeedRemovalSuggestions" v-html="filteredWeedRemovalSuggestions"></p>
        <p v-else>No suggestions available.</p>
      </el-card>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import { mapGetters } from 'vuex';

  export default {
    name: "Content",
    data() {
      return {
        server_url: "http://127.0.0.1:5003",  // Backend server URL for uploading files and retrieving predictions
        activeName: "first",  // Default active tab
        url_2: "",  // Prediction result image URL
        loading: false,  // Loading indicator
        showbutton: true,  // Controls the visibility of the upload button
        percentage: 0,  // Progress percentage for AI prediction
        dialogTableVisible: false,  // Controls the visibility of the progress dialog
        allImageUrls: [],  // List of URLs for all uploaded images
        currentImageIndex: 0,  // Index of the currently displayed image
        imageNames: [],  // List of image names corresponding to the uploaded images
        feature_list: [],  // List of key-value pairs for image information
        weedRemovalSuggestions: "",  // Weed removal suggestions from AI analysis
      };
    },
    computed: {
      ...mapGetters(['getUsername']),
      // Get the current image URL based on the selected index
      currentImageUrl() {
        return this.allImageUrls[this.currentImageIndex] || '';
      },
      // Filter weed removal suggestions to remove unwanted characters
      filteredWeedRemovalSuggestions() {
        return this.weedRemovalSuggestions.replace(/\*.*?\*/g, '');  // Removes text between '*' characters
      }
    },
    methods: {
      // Triggers the file upload input
      true_upload() {
        this.$refs.upload.click();
      },
      // Handles file upload and initiates AI prediction
      update(e) {
        this.dialogTableVisible = true;
        this.loading = true;
        let file = e.target.files[0];
        let param = new FormData();
        param.append("file", file, file.name);

        let config = {
          headers: { "Content-Type": "multipart/form-data" }
        };

        axios
          .post(this.server_url + "/upload", param, config)
          .then((response) => {
            if (response.data.status === 1) {
              this.allImageUrls = response.data.input_image_urls;
              this.imageNames = response.data.spectrum_names;
              this.url_2 = response.data.predicted_mask_url;

              this.feature_list = Object.entries(response.data.image_info).map(([key, value]) => {
                const formattedKey = key.replace(/([A-Z])/g, ' $1').replace(/_/g, ' ').replace(/^./, str => str.toUpperCase());
                const displayValue = Array.isArray(value) ? value.join(' x ') : value;
                return [formattedKey, displayValue];
              });

              this.weedRemovalSuggestions = response.data.weed_removal_suggestions;
              this.loading = false;
              this.dialogTableVisible = false;
            } else {
              this.showError("Failed to process the image.");
            }
          })
          .catch((error) => {
            this.showError("An error occurred while uploading the file.");
            this.loading = false;
            this.dialogTableVisible = false;
          });
      },
      // Show an error notification
      showError(message) {
        this.$notify({
          title: "Error",
          message: message,
          type: "error",
          duration: 5000
        });
      }
    }
  };
</script>

<style scoped>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  .box-card {
    width: 100%;
  }

  .error {
    margin: 100px auto;
    width: 50%;
    padding: 10px;
    text-align: center;
  }

  .download_bt {
    padding: 10px 16px !important;
  }

  #Content {
    width: 85%;
    margin: 15px auto;
  }

  .how-to-use {
    width: 100%;
  }

  .no-data {
    color: #c0c4cc;
    font-size: 14px;
    text-align: center;
    line-height: 250px;
  }

  #info_weed2 {
    margin-top: 20px;
    text-align: left;
  }

  .img_info_1 {
    height: 30px;
    width: 275px;
    text-align: center;
    background-color: #6ec2b1;
    line-height: 30px;
  }

  .image_1 {
    width: 275px;
    height: 260px;
    background: #ffffff;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }
</style>
