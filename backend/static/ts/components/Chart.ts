export default class Chart {
    baseElement: HTMLElement
    constructor(baseElement: HTMLElement) {
        this.baseElement = baseElement

        var chartData = baseElement.getAttribute('chat-data')
        if (!chartData) {
            throw new Error("Chart data must me installed")
        }
    }

}
