const filterItems = document.querySelectorAll('.filters__parametres .parameter-item');

function toggleFilter() {
    let checkmarks = this.querySelectorAll('.checkmark');
    for (let i = 0; i < 2; i++) {
        checkmarks[i].classList.toggle('selected')
    }
}

for (let i = 0, len = filterItems.length; i < len; i++) {
    filterItems[i].addEventListener('click', toggleFilter);
};


