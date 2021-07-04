import { Chart } from 'chart.js'

export default class ChartComponent {
    baseElement: HTMLElement

    constructor(baseElement: HTMLElement) {
        this.baseElement = baseElement

        var chartDates = baseElement.getAttribute('data-dates')
        if (!chartDates) {
            throw new Error("Chart data must me installed")
        }
        var chartValues = baseElement.getAttribute('data-prices')
        if (!chartValues) {
            throw new Error("Chart data must me installed")
        }
        this.renderChart(baseElement.querySelector('#canvas')!, [], [])
    }

    renderChart(element: HTMLCanvasElement, labels: Array<Date>, values: Array<Number>) {
        new Chart(element, {
            type: 'bar',
            data: {
                labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            }
        })
    }
}
