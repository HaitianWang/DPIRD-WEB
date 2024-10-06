<!--
This component is part of the DPIRD AgriVision project, called "Time Capsule."
It allows users to select a field area and specific plot to view historical data displayed in a vertical timeline format.
The timeline provides an overview of weed management and technological advancements across multiple years for the selected field area and plot.
If the selected location and plot do not have data, a message indicating "No data" will be displayed.
The component uses Vue.js for data binding and conditionally rendering the timeline content based on user input.
-->

<template>
  <div>
    <div id="dropdown-box">
      <h3>Time Capsule: choose your field area:</h3>
      <!-- Dropdown for selecting location -->
      <select v-model="selectedLocation" class="dropdown">
        <option value="Kondinin">Kondinin</option>
        <option value="Rockingham">Rockingham</option>
        <option value="Perth">Perth</option>
        <option value="Bunbury">Bunbury</option>
      </select>
      <!-- Dropdown for selecting specific plot -->
      <select v-model="selectedOption" class="dropdown">
        <option value="E2">E2</option>
        <option value="E8">E8</option>
        <option value="E9">E9</option>
      </select>
    </div>

    <!-- Conditionally render timeline or "No data" message -->
    <div v-if="selectedLocation === 'Kondinin' && selectedOption === 'E2'">
      <!-- Vertical timeline starts here -->
      <div class="timeline">
        <div class="timeline-item">
          <div class="timeline-time">2020</div>
          <div class="timeline-content">
            <img src="@/assets/2020.png" alt="2020 Image">
            <div class="timeline-text">
              <p>
                In 2020, the implementation of integrated weed management strategies saw a significant reduction in herbicide-resistant weed populations. Farmers adopted a mix of mechanical weeding, crop rotation, and targeted herbicide applications, which together enhanced the sustainability of weed control efforts.
              </p>
            </div>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-time">2021</div>
          <div class="timeline-content">
            <img src="@/assets/2021.png" alt="2021 Image">
            <div class="timeline-text">
              <p>
                In 2021, advancements in weed detection technology allowed for more precise and efficient targeting of problem areas. Drones equipped with multispectral cameras were deployed to monitor crop fields, enabling real-time analysis and rapid response to emerging weed infestations.
              </p>
            </div>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-time">2022</div>
          <div class="timeline-content">
            <img src="@/assets/2022.png" alt="2022 Image">
            <div class="timeline-text">
              <p>
                In 2022, a focus on biological control methods introduced beneficial insects and microbial agents into the fields. These natural enemies targeted specific weed species, reducing their prevalence without the need for chemical interventions.
              </p>
            </div>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-time">2023</div>
          <div class="timeline-content">
            <img src="@/assets/2023.png" alt="2023 Image">
            <div class="timeline-text">
              <p>
                In 2023, precision agriculture techniques were further refined to enhance weed management. The integration of AI-driven tools allowed for predictive modeling of weed growth patterns, enabling preemptive measures to be taken before infestations could establish.
              </p>
            </div>
          </div>
        </div>
      </div>
      <!-- Vertical timeline ends here -->
    </div>

    <div v-else>
      <p style="text-align: center; font-size: 18px; color: #555;">Sorry, no data for now</p>
    </div>

  </div>
</template>

<script>
  export default {
    name: 'TimeCapsule',
    data() {
      return {
        selectedLocation: 'Kondinin',  // Default location value
        selectedOption: 'E2'  // Default plot option value
      };
    }
  };
</script>

<style scoped>
  /* Styling for dropdown section */
  #dropdown-box {
    display: flex;
    align-items: center;
    margin-left: 50px;
    margin-bottom: 20px; /* Space between dropdowns and timeline */
  }

  h3 {
    margin-right: 20px;
    margin-bottom: 0;
  }

  .dropdown {
    width: 200px;
    height: 40px;
    font-size: 16px;
    margin-right: 10px;
  }

  /* Timeline styling */
  .timeline {
    position: relative;
    padding: 20px 50px;
    list-style: none;
    margin-left: 50px;
  }

  .timeline::before {
    content: '';
    position: absolute;
    left: 30px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #d9f0ea;  /* Vertical line color */
  }

  .timeline-item {
    margin-bottom: 30px;
    position: relative;
  }

  .timeline-time {
    padding: 10px 20px;
    background: #6ec2b1;  /* Background for year */
    color: white;
    border-radius: 50px;
    font-weight: bold;
    text-align: center;
    position: relative;
    left: -40px;
    width: 80px;
  }

  .timeline-content {
    display: flex;
    align-items: center;
    margin-left: 80px;
    padding: 10px 20px;
    background: #d9f0ea;  /* Background for content */
    border-radius: 8px;
    position: relative;
  }

  .timeline-content img {
    max-width: 300px;
    display: block;
    margin-right: 20px;
  }

  .timeline-text {
    flex: 1;
  }

  .timeline-text p {
    margin-top: 0;
    font-size: 14px;
    line-height: 1.5;
  }
</style>
