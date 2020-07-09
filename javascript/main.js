hljs.initHighlightingOnLoad();

const modified = document.querySelector('#modified') ? document.querySelector('#modified') : null;
const lastModified = '2020 Július 9.'

modified != null ? modified.textContent = 'Utolsó modósítás: ' + lastModified : null;

const arrow = document.querySelector('#arr');
const firstPar = document.querySelector('#firstPar');

function debounce(func, wait = 10, immediate = true) {
    var timeout;
    return function () {
        var context = this,
            args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

function checkPos(e) {
    const appearPos = firstPar.offsetTop;
    
    if (window.scrollY > appearPos) {
        arrow.classList.add('show');
    } else if (window.scrollY < appearPos) {
        arrow.classList.remove('show');
    }
}

window.addEventListener('scroll', debounce(checkPos));