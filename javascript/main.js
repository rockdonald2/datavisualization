hljs.initHighlightingOnLoad();

const modified = document.querySelector('#modified') ? document.querySelector('#modified') : null;
const lastModified = '2020 Július 13.'

modified != null ? modified.textContent = 'Utolsó modósítás: ' + lastModified : null;

/* Nyíl megjelenése */

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

/* Másolás gomb a kódrészleteknél */

const gomb = document.querySelectorAll('#copy');

function masolas(e) {
    /* megszerezzük a kód tartalmát */
    const kod = e.target.parentNode.childNodes[0];

    /* egy rejtett textarea DOM elem */
    let copyTextarea = document.createElement("textarea");
    copyTextarea.style.position = "fixed";
    copyTextarea.style.opacity = "0";
    copyTextarea.textContent = kod.textContent;

    /* hozzáadjuk a clipboardhoz, és töröljük a rejtett elemet a DOM-ból */
    document.body.appendChild(copyTextarea);
    copyTextarea.select();
    document.execCommand("copy");
    document.body.removeChild(copyTextarea);
}

gomb.forEach((g) => g.addEventListener('click', masolas));