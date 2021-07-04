export default class DemoFill {
  baseElement: HTMLElement;

  constructor(baseElement: HTMLElement) {
    this.baseElement = baseElement;

    this.baseElement.addEventListener('click', () => {
      let email = this.baseElement.getAttribute('data-email')!;
      let password = this.baseElement.getAttribute('data-password')!;
      
      let emailField = document.getElementById("emailField") as HTMLInputElement;
      if (emailField) {
        emailField.value = email;
      }

      let passwordField = document.getElementById("passwordField") as HTMLInputElement;
      if (passwordField) {
        passwordField.value = password;
      }
    });
  }
}
