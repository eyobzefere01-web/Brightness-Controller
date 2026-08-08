const form = document.querySelector('#brightness-form');
const main_container = document.querySelector('.main-container');
const reg_page = document.querySelector('.reg_db_password');
const msg = document.querySelector('.message')

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const send = await fetch('/adjust-brightness', {
    method: 'POST',
    body: formData
  });
  const receive = await send.json();
  if (receive.status == 404){
    main_container.classList.add('disappear');
    reg_page.classList.remove('disappear');
    reg_page.addEventListener('submit', async (event) => {
      event.preventDefault();
      const passwordData = new FormData(event.target);
      const send_password = await fetch('/rec_sudo',{
        method: 'POST',
        body: passwordData
      });
      const validation_res = await send_password.json()
      if (validation_res.status == 'error'){
        msg.textContent = validation_res.message;
      }
    })
  }else if (receive.status == 200){
    msg.textContent = 'Successfully Changed';
    msg.classList.remove('error')
    msg.classList.add('successful');
    
  }else if (receive.status == 500){
    msg.textContent = 'Invalid input. Enter only Integer value!';
    msg.classList.remove('successful')
    msg.classList.add('error')
  }else{
    alert('Unknown Status')
  }
});