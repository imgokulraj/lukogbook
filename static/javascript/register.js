const submit = document.querySelector('#register-form-submit')
submit.addEventListener('click' , (e) => {
    e.preventDefault() 
    document.forms["registerform"].submit();
})


const labels = document.querySelectorAll('.form-control label')

labels.forEach(label => {
    label.innerHTML = label.innerText
        .split('')
        .map((letter, idx) => `<span style="transition-delay:${idx * 50}ms">${letter}</span>`)
        .join('')
})