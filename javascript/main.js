const modified = document.querySelector('#modified') ? document.querySelector('#modified') : null;
const lastModified = '2020 Július 5.'

modified != null ? modified.textContent = 'Utolsó modósítás: ' + lastModified : null;