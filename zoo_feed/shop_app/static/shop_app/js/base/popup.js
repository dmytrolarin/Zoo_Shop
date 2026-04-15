const popupLinks = document.querySelectorAll('.popup-link');
const body = document.querySelector('body');
const lockPadding = document.querySelectorAll('.lock-padding');

const headerBurger = document.querySelector('.header__burger');
const headerMenu = document.querySelector('.header__menu')

let unlock = true;

const timeout = 500;

// Handle clicks on links that open popups.
if (popupLinks.length > 0) {
    for (let index = 0; index < popupLinks.length; index++) {
        const popupLink = popupLinks[index];
        popupLink.addEventListener('click', function (e){
            const popupName = popupLink.getAttribute('popup-id');
            const curentPopup = document.getElementById(popupName);
            popupOpen(curentPopup);
        });
    }
}

const popupCloseIcon = document.querySelectorAll('.close-popup');
// Handle clicks on popup close buttons.
if (popupCloseIcon.length > 0) {
    for (let index = 0; index < popupCloseIcon.length; index++){
        const el = popupCloseIcon[index];
        el.addEventListener('click', function (e) {
            popupClose(el.closest('.popup'));
            e.preventDefault();
        });
    }
}
// Open a popup.
function popupOpen(currentPopup){
    if (currentPopup && unlock) {
        const popupActive = document.querySelector('.popup.open');
        console.log(popupActive);
        if (popupActive) {
            popupClose(popupActive, false);  
        }
         else {
            bodyLock();
        }
        currentPopup.classList.add('open');
        headerBurger.classList.remove('active');
        headerMenu.classList.remove('active');
        currentPopup.addEventListener('click', function (e) {
            if (!e.target.closest('.popup__content')){
                popupClose(e.target.closest('.popup'));
            }
        });
    }   
}
// Close a popup.
function popupClose(popupActive, doUnlock=true){
    if  (unlock){
        popupActive.classList.remove('open');
        if (doUnlock) {
            bodyUnlock();
        }
    }
}
// Lock page scrolling.
function bodyLock(){
    const lockPaddingValue = window.innerWidth - document.querySelector('.wrapper').offsetWidth + 'px'

    if (lockPadding.length > 0){
        for (let index = 0; index < lockPadding.length; index++){
            const el = lockPadding[index];
            el.style.paddingRight = lockPaddingValue;
        }
    }
    body.style.paddingRight = lockPaddingValue;
    body.classList.add('lock');

    unlock = false;
    setTimeout(function (){
        unlock = true
    }, timeout);
}

// Unlock page scrolling.
function bodyUnlock(){
    setTimeout(function(){
        if (lockPadding.length > 0){
            for (let index = 0; index < lockPadding.length; index++){
                const el = lockPadding[index];
                el.style.paddingRight = '0px';
            }
        }
        body.style.paddingRight ='0px';
        body.classList.remove('lock');
    }, timeout);

    unlock = false;
    setTimeout(function (){
        unlock = true
    }, timeout);
}
// Close the popup window with the Escape key.
document.addEventListener('keydown', function (e){
    if (e.which === 27){
        const popupActive = document.querySelector('.popup.open');
        popupClose(popupActive);
    }
});



