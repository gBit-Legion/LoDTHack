<template>
  <div class="border-idealRed p-2 border-4 rounded-lg w-full shadow-cards">
    <div id="chart">
      <div class="toolbar">
        <button
          id="one_month"
          @click="updateData('one_month')"
          :class="{ active: selection === 'one_month' }"
        >
          1M
        </button>

        <button
          id="six_months"
          @click="updateData('six_months')"
          :class="{ active: selection === 'six_months' }"
        >
          6M
        </button>

        <button
          id="one_year"
          @click="updateData('one_year')"
          :class="{ active: selection === 'one_year' }"
        >
          1Y
        </button>

        <button
          id="ytd"
          @click="updateData('ytd')"
          :class="{ active: selection === 'ytd' }"
        >
          YTD
        </button>

        <button
          id="all"
          @click="updateData('all')"
          :class="{ active: selection === 'all' }"
        >
          ALL
        </button>
      </div>

      <div id="chart-timeline">
        <apexchart
          type="area"
          height="350"
          ref="chart"
          :options="chartOptions"
          :series="series"
        ></apexchart>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  computed:{
    series_data(){
      let datas = []
      this.data_chart.forEach(element => {
        datas.push(element)
        console.log(datas)
      })
      return datas;
    }
  },
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [{
            data: 
            Object.values(this.data_chart)
      
          }],
      chartOptions: {
        chart: {
          id: "area-datetime",
          type: "area",
          height: 350,
          zoom: {
            autoScaleYaxis: true,
          },
        },
        annotations: {
          yaxis: [
            {
              y: 30,
              borderColor: "#999",
              label: {
                show: true,
                text: "Support",
                style: {
                  color: "#fff",
                  background: "#00E396",
                },
              },
            },
          ],
          xaxis: [
            {
              x: new Date("14 Nov 2012").getTime(),
              borderColor: "#999",
              yAxisIndex: 0,
              label: {
                show: true,
                text: "Rally",
                style: {
                  color: "#fff",
                  background: "#775DD0",
                },
              },
            },
          ],
        },
        dataLabels: {
          enabled: false,
        },
        markers: {
          size: 0,
          style: "hollow",
        },
        xaxis: {
          type: "datetime",
          min: new Date("01 Mar 2012").getTime(),
          tickAmount: 6,
        },
        tooltip: {
          x: {
            format: "dd MMM yyyy",
          },
        },
        fill: {
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 100],
          },
        },
      },

      selection: "one_year",
    };
  },
  methods: {
    updateData: function (timeline) {
      this.selection = timeline;

      switch (timeline) {
        case "one_month":
          this.$refs.chart.zoomX(
            new Date("28 Jan 2013").getTime(),
            new Date("27 Feb 2013").getTime()
          );
          break;
        case "six_months":
          this.$refs.chart.zoomX(
            new Date("27 Sep 2012").getTime(),
            new Date("27 Feb 2013").getTime()
          );
          break;
        case "one_year":
          this.$refs.chart.zoomX(
            new Date("27 Feb 2012").getTime(),
            new Date("27 Feb 2013").getTime()
          );
          break;
        case "ytd":
          this.$refs.chart.zoomX(
            new Date("01 Jan 2013").getTime(),
            new Date("27 Feb 2013").getTime()
          );
          break;
        case "all":
          this.$refs.chart.zoomX(
            new Date("23 Jan 2012").getTime(),
            new Date("27 Feb 2013").getTime()
          );
          break;
        default:
      }
    },
  },
  props: {
    data_chart: Object,
  },
  mounted() {
    console.log((toRaw(Object.values(this.data_chart))));
  },
};
</script>

<style></style>
