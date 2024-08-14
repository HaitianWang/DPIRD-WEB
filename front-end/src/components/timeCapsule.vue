<template>
  <div>
    <div id="dropdown-box">
      <h3>Time Capsule: choose your field area:</h3>
      <select v-model="selectedLocation" class="dropdown">
        <option value="Kondinin">Kondinin</option>
        <option value="Rockingham">Rockingham</option>
        <option value="Perth">Perth</option>
        <option value="Bunbury">Bunbury</option>
      </select>
      <select v-model="selectedOption" class="dropdown">
        <option value="E2">E2</option>
        <option value="E8">E8</option>
        <option value="E9">E9</option>
      </select>
    </div>

    <!-- 条件渲染时间轴或无数据消息 -->
    <div v-if="selectedLocation === 'Kondinin' && selectedOption === 'E2'">
      <!-- 竖直时间轴开始 -->
      <div class="timeline">
        <div class="timeline-item">
          <div class="timeline-time">2020</div>
          <div class="timeline-content">
            <img src="@/assets/2020.png" alt="2020 Image">
            <div class="timeline-text">
              <p>
                In 2020, the implementation of integrated weed management strategies saw a significant reduction in herbicide-resistant weed populations. Farmers adopted a mix of mechanical weeding, crop rotation, and targeted herbicide applications, which together enhanced the sustainability of weed control efforts. This holistic approach not only controlled the existing weed populations but also helped prevent the development of new resistant strains. Throughout the year, educational programs were conducted to train farmers in best practices, ensuring that these methods were adopted widely and effectively. The results were promising, with many fields reporting a drastic decline in weed-related crop losses, setting a new benchmark for future weed management initiatives.
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
                In 2021, advancements in weed detection technology allowed for more precise and efficient targeting of problem areas. Drones equipped with multispectral cameras were deployed to monitor crop fields, enabling real-time analysis and rapid response to emerging weed infestations. This technology not only reduced labor costs but also minimized the environmental impact of herbicide use by applying treatments only where necessary. The integration of these technologies into everyday farming practices marked a significant leap forward, allowing for the continuous monitoring of vast agricultural lands with minimal human intervention. The success of these technologies inspired further innovations, pushing the boundaries of precision agriculture and setting the stage for even more advanced solutions in the years to come.
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
                In 2022, a focus on biological control methods introduced beneficial insects and microbial agents into the fields. These natural enemies targeted specific weed species, reducing their prevalence without the need for chemical interventions. This year marked a turning point in the adoption of environmentally friendly weed management practices, promoting biodiversity and soil health across agricultural landscapes. Extensive field trials were conducted to evaluate the effectiveness of these biological agents, with results showing a consistent decrease in weed populations across different crop types. The success of these trials led to widespread adoption of biological control methods, further reducing the reliance on chemical herbicides and contributing to the overall sustainability of agricultural ecosystems.
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
                In 2023, precision agriculture techniques were further refined to enhance weed management. The integration of AI-driven tools allowed for predictive modeling of weed growth patterns, enabling preemptive measures to be taken before infestations could establish. This proactive approach, combined with continued use of biological and mechanical controls, ensured that crop yields remained high despite the challenges posed by weed resistance. Additionally, collaboration between researchers and farmers led to the development of customized weed management plans tailored to specific regions, maximizing the effectiveness of interventions and minimizing the risk of resistance development. The year ended with record-breaking yields in many areas, demonstrating the power of combining traditional farming wisdom with cutting-edge technology.
              </p>
            </div>
          </div>
        </div>
      </div>
      <!-- 竖直时间轴结束 -->
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
        selectedLocation: 'Kondinin', // 默认值
        selectedOption: 'E2' // 默认值
      };
    }
  };
</script>

<style scoped>
  #dropdown-box {
    display: flex;
    align-items: center;
    margin-left: 50px;
    margin-bottom: 20px; /* 添加下拉框与时间轴之间的间距 */
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

  /* 时间轴样式 */
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
    background: #d9f0ea;
  }

  .timeline-item {
    margin-bottom: 30px;
    position: relative;
  }

  .timeline-time {
    padding: 10px 20px;
    background: #6ec2b1;
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
    background: #d9f0ea;
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

  .report-link {
    color: #3F51B5;
    text-decoration: none;
    font-weight: bold;
  }

  .report-link:hover {
    text-decoration: underline;
  }
</style>
