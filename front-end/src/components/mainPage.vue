<!--
This is the main page of the DPIRD AgriVision application.
It provides an overview of the project's primary objectives, focusing on the use of multispectral imaging and deep learning to differentiate between crop types and weeds.
The page displays a header with an image and includes a detailed description of the project's goals, emphasizing its potential for precision agriculture and farm management support.
-->

<template>
  <div class="main-page">
    <!-- Section displaying an image related to the project -->
    <div class="field-section">
      <img src="@/assets/7.png" alt="image" class="field-image">
    </div>

    <!-- Section containing the project's detailed description and objectives -->
    <div class="intro-text">
      <p>
        The primary objective of this project is to conceive, develop, and implement the application system
        named DPIRD AgriVision, a robust and integrated system that harnesses the power of advanced
        multispectral imaging combined with sophisticated deep learning techniques. This system will be
        tailored to accurately differentiate between various crop types and weed species, enabling precise
        monitoring and assessment of the extent and severity of crop damage. By fusing these insights
        with GIS data, DPIRD AgriVision will not only visualize the impacts on a macro scale but also
        generate detailed analytical reports and actionable recommendations for effective farm
        management. The ultimate aim is to support farmers in the Kondinin region—and potentially
        beyond—in implementing efficacious management strategies to minimize economic losses.
        Through its deployment on cloud infrastructure, DPIRD AgriVision promises accessibility and
        utility to users across diverse locations, offering a scalable solution in the domain of precision
        agriculture.
      </p>
    </div>
  </div>
</template>

<script>
  export default {
    name: "mainPage",
    created() {
      // Emit events to ensure the header and footer are displayed on the main page
      this.$emit('header', true);
      this.$emit('footer', true);
    },
  };
</script>

<style scoped>
  /* Main page styling */
  .main-page {
    text-align: center;
    padding: 20px;
  }

  /* Styling for the image section */
  .field-section {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
  }

  /* Styling for the field image */
  .field-image {
    width: 95%; /* Adjust the width as needed */
    height: auto;
    margin-right: 20px;
  }

  /* Styling for the text introducing the project */
  .intro-text {
    margin: 30px;
    font-size: 1.2em;
    line-height: 1.6em;
    color: #333;
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 8px;
    text-align: left;
  }
</style>
