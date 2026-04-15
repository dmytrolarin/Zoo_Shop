let elements = document.getElementsByClassName('phone-number-field');  
for (let i = 0; i < elements.length; i++) {
    new IMask(elements[i], {
    mask: '+{380}(00)000-00-00',
    });
}