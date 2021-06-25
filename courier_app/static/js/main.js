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


    // format price and percent 0.20 to 20.00%
    var mountsEl = document.querySelectorAll('.mount');
    var percentsEl = document.querySelectorAll('.percent');

    const formatMount = (value) => {
        if (typeof value != 'number') return;
        var options = { style: 'currency', currency: 'PEN', minimumFractionDigits: 2};
        return value.toLocaleString('es-PE', options);
    }
    const formatPercent = (value) => {
        if (typeof value != 'number') return;
        var options = { style: 'percent', minimumFractionDigits: 2 };
        return value.toLocaleString('es-PE', options);
    }

    for (mountEl of mountsEl) {
        mountEl.textContent = formatMount(+mountEl.textContent);
    }
    for (percentEl of percentsEl) {
        percentEl.textContent = formatPercent(+percentEl.textContent);
    }

})()