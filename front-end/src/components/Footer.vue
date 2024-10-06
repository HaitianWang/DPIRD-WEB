<!--
This is a simple footer component for the DPIRD AgriVision frontend.
The main purpose of this component is to display a footer message (e.g., "2024 DPIRD AgriVision") at the bottom of the page.
The component uses Vue.js for managing the data and rendering the message dynamically.
The CSS styles ensure the footer is centered, padded, and has specific dimensions and colors.
-->

<template>
  <div id="Footer">
    <!-- Displaying the footer message -->
    <p>{{ msg }}</p>
  </div>
</template>

<script>
  export default {
    name: "Footer",
    data() {
      return {
        msg: "2024 DPIRD AgriVision",  // The footer message to display
      };
    },
  };
</script>

<style scoped>
  #Footer {
    /* Footer styling */
    padding: 6px;
    border-radius: 5px;
    width: 80%;
    height: 80px;
    margin: 20px auto;
    margin-top: 140px;
  }

  p {
    /* Styling for the text inside the footer */
    color: #36471f;
    text-align: center;
    margin: 30px auto;
    font-size: 1.1em;
  }
</style>
