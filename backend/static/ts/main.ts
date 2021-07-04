// Styles
import '../scss/main.scss'

import DemoFill from './demo';
import ChartComponent from "./components/Chart";

let demoFillButtons = [].slice.call(document.querySelectorAll('.DemoFill')) as HTMLButtonElement[];
demoFillButtons.forEach(button => {
    new DemoFill(button);
});

window.document.querySelectorAll('.chart-component').forEach(element=>{
    new ChartComponent(element as HTMLElement)
})
