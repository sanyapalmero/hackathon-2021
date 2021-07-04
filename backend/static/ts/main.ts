// Styles
import '../scss/main.scss'

import DemoFill from './demo';


let demoFillButtons = [].slice.call(document.querySelectorAll('.DemoFill')) as HTMLButtonElement[];
demoFillButtons.forEach(button => {
    new DemoFill(button);
});
