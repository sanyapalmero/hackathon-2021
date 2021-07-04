import Chart from 'chart.js/auto';

export default class ChartComponent {
    baseElement: HTMLElement

    constructor(baseElement: HTMLElement) {
        this.baseElement = baseElement

        let rowChartDates = baseElement.getAttribute('data-dates');
        if (!rowChartDates) {
            throw new Error("Chart data must me installed")
        }
        let chartDates = rowChartDates.split(",");

        let rowChartValues = baseElement.getAttribute('data-prices');
        if (!rowChartValues) {
            throw new Error("Chart data must me installed")
        }
        let chartValues = rowChartValues.split(",").map((value) => Number(value));

        this.renderChart(baseElement.querySelector('#canvas')!, chartDates, chartValues)
    }

    renderChart(element: HTMLCanvasElement, labels: Array<string>, values: Array<Number>) {
        new Chart(element, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: "Цена",
                    data: values,
                    backgroundColor: 'rgba(255, 99, 132, 1)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    pointRadius: 4,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        })
    }
}
