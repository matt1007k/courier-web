(function(){
    const password_group = document.querySelectorAll('.form-group-password');
    password_group.forEach(group_password => {
    const show_password = group_password.querySelector('#show-password');
    const input_password = group_password.querySelector('input[type="password"]');
    show_password.addEventListener('click', (ev) => {
        if (input_password.type == 'password'){
        input_password.type = 'text';
        show_password.classList.add('active');
        show_password.textContent = 'ocultar';
        } else {
        input_password.type = 'password';
        show_password.classList.remove('active');
        show_password.textContent = 'mostrar';
        }
    });
    });

})()