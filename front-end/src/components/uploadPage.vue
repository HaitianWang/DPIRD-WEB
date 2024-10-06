<template>
  <div id="Content" style="display: flex; flex-direction: column; align-items: center;">
    <!-- How to Use Section -->
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

    <!-- Existing Dialog -->
    <el-dialog title="AI Prediction in Progress" :visible.sync="dialogTableVisible" :show-close="false"
               :close-on-press-escape="false" :append-to-body="true" :close-on-click-modal="false" :center="true">
      <el-progress :percentage="percentage"></el-progress>
      <span slot="footer" class="dialog-footer">Please wait patiently for about 3 seconds</span>
    </el-dialog>

    <!-- CT Images Section -->
    <div id="CT" style="width: 100%; margin-bottom: 20px;">
      <el-card id="CT_image_1" class="box-card" style="
            border-radius: 8px;
            width: 100%;
            margin-bottom: 20px;
          ">
        <div class="demo-image__preview1">
          <div v-loading="loading" element-loading-text="Uploading Image" element-loading-spinner="el-icon-loading">
            <el-image :src="currentImageUrl" class="image_1" :preview-src-list="allImageUrls"
                      style="border-radius: 3px 3px 0 0">
              <div slot="error">
                <div slot="placeholder" class="error">
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

    <!-- Analysis Section -->
    <div id="info_weed" style="width: 100%;">
      <el-card style="border-radius: 8px">
        <div slot="header" class="clearfix">
          <span>Analysis</span>
          <el-button style="margin-left: 35px" v-show="!showbutton" type="primary" icon="el-icon-upload"
                     class="download_bt" v-on:click="true_upload2">
            Re-select Image
            <input ref="upload2" style="display: none" name="file" type="file" @change="update" />
          </el-button>
        </div>
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
    <div id="info_weed2" style="width: 100%;">
      <!-- Suggestions Section -->
      <el-card style="border-radius: 8px; margin-bottom: 20px;">
        <div slot="header" class="clearfix">
          <span>Weed Removal Suggestions</span>
        </div>
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
        server_url: "http://127.0.0.1:5003",
        activeName: "first",
        active: 0,
        centerDialogVisible: true,
        kepuDialogVisible: false,
        url_1: "",
        url_2: "",
        textarea: "",
        srcList: [],
        srcList1: [],
        feature_list: [],
        feature_list_1: [],
        feat_list: [],
        url: "",
        visible: false,
        wait_return: "Waiting for upload",
        wait_upload: "Waiting for upload",
        loading: false,
        weedRemovalSuggestions: "",
        table: false,
        isNav: false,
        showbutton: true,
        percentage: 0,
        fullscreenLoading: false,
        opacitys: {
          opacity: 0,
        },
        dialogTableVisible: false,
        allImageUrls: [],
        currentImageIndex: 0,
        imageNames: [],
      };
    },
    computed: {
      ...mapGetters(['getUsername']),
      currentImageUrl() {
        return this.allImageUrls[this.currentImageIndex] || '';
      },
      currentImageName() {
        return this.imageNames[this.currentImageIndex] || '';
      },
      filteredWeedRemovalSuggestions() {
        return this.weedRemovalSuggestions.replace(/\*.*?\*/g, '');
      }
    },
    created: function () {
      document.title = "DPIRD AgriVision";
    },
    methods: {
      previousImage() {
        if (this.currentImageIndex > 0) {
          this.currentImageIndex--;
        }
      },
      nextImage() {
        if (this.currentImageIndex < this.allImageUrls.length - 1) {
          this.currentImageIndex++;
        }
      },
      showError(message) {
        this.$notify({
          title: "Error",
          message: message,
          type: "error",
          duration: 5000
        });
      },
      true_upload() {
        this.$refs.upload.click();
      },
      true_upload2() {
        this.$refs.upload2.click();
      },
      showJiaochen() {
        this.centerDialogVisible = true;
      },
      showKepu() {
        this.kepuDialogVisible = true;
      },
      handleClose(done) {
        this.$confirm("Confirm to close?")
          .then((_) => {
            done();
          })
          .catch((_) => { });
      },
      next() {
        this.active++;
      },

      getObjectURL(file) {
        var url = null;
        if (window.createObjcectURL != undefined) {
          url = window.createOjcectURL(file);
        } else if (window.URL != undefined) {
          url = window.URL.createObjectURL(file);
        } else if (window.webkitURL != undefined) {
          url = window.webkitURL.createObjectURL(file);
        }
        return url;
      },

      update(e) {
        this.percentage = 0;
        this.dialogTableVisible = true;
        this.url_1 = "";
        this.url_2 = "";
        this.srcList = [];
        this.srcList1 = [];
        this.wait_return = "";
        this.wait_upload = "";
        this.feature_list = [];
        this.fullscreenLoading = true;
        this.loading = true;
        this.showbutton = false;

        let file = e.target.files[0];
        let param = new FormData();
        param.append("file", file, file.name);

        let config = {
          headers: { "Content-Type": "multipart/form-data" }
        };

        var timer = setInterval(() => {
          this.myFunc();
        }, 30);

        axios
          .post(this.server_url + "/upload", param, config)
          .then((response) => {
            if (response.data.status === 1) {
              this.allImageUrls = response.data.input_image_urls;
              this.imageNames = response.data.spectrum_names;
              this.currentImageIndex = 0;


              this.url_2 = response.data.predicted_mask_url;
              this.srcList1.push(this.url_2);

              this.fullscreenLoading = false;
              this.loading = false;

              if (response.data.image_info) {
                this.feature_list = Object.entries(response.data.image_info).map(([key, value]) => {
                  // Check if the value is an array, if so, join it
                  const displayValue = Array.isArray(value) ? value.join(' x ') : value;
                  // Convert key from camelCase or snake_case to Title Case
                  const formattedKey = key.replace(/([A-Z])/g, ' $1')
                    .replace(/_/g, ' ')
                    .replace(/^./, str => str.toUpperCase());
                  return [formattedKey, displayValue];
                });
              }
              this.weedRemovalSuggestions = response.data.weed_removal_suggestions;
              this.dialogTableVisible = false;
              this.percentage = 0;
              this.notice1();
            } else {
              this.showError("Failed to process the image.");
            }
          })
          .catch((error) => {
            console.error("Error uploading file:", error);
            this.fullscreenLoading = false;
            this.loading = false;
            this.dialogTableVisible = false;
            this.showError("An error occurred while uploading the file.");
            clearInterval(timer);
          });
      },
      myFunc() {
        if (this.percentage + 33 < 99) {
          this.percentage = this.percentage + 33;
        } else {
          this.percentage = 99;
        }
      },
      drawChart() { },
      notice1() {
        this.$notify({
          title: "Prediction Successful",
          message: "Click the image to view the large image",
          duration: 0,
          type: "success",
        });
      },
      notice2() {
        this.$notify({
          title: "Suspect you have skin cancer?",
          message: "",
          duration: 0,
          type: "success",
        });
      },
    },
    mounted() {
      this.drawChart();
    },
  };
</script>

<style>
  .el-button {
    padding: 12px 20px !important;
  }

  #hello p {
    font-size: 15px !important;
  }

  .n1 .el-step__description {
    padding-right: 20%;
    font-size: 14px;
    line-height: 20px;
  }
</style>

<style scoped>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both;
  }

  .box-card {
    width: 100%;
  }

  .divider {
    width: 50%;
  }

  #CT {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
  }

  #CT_image_1 {
    width: 90%;
    height: 40%;
    margin: 0px auto;
    padding: 0px auto;
    margin-right: 180px;
    margin-bottom: 0px;
    border-radius: 4px;
  }

  #CT_image {
    margin-bottom: 60px;
    margin-left: 30px;
    margin-top: 5px;
  }

  .image_1 {
    width: 275px;
    height: 260px;
    background: #ffffff;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }

  .img_info_1 {
    height: 30px;
    width: 275px;
    text-align: center;
    background-color: #6ec2b1;
    line-height: 30px;
  }

  .demo-image__preview1 {
    width: 250px;
    height: 290px;
    margin: 20px 60px;
    float: left;
  }

  .demo-image__preview2 {
    width: 250px;
    height: 290px;
    margin: 20px 460px;
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

  #info_weed {
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

</style>
