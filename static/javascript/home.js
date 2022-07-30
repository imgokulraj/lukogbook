const submit = document.querySelector('#login-form-submit') 
        submit.addEventListener('click' , (e) => { 
            e.preventDefault() 
            console.log('hi') 
            document.forms['loginform'].submit()
        })

        
const labels = document.querySelectorAll('.form-control label')

labels.forEach(label => {
    label.innerHTML = label.innerText
        .split('')
        .map((letter, idx) => `<span style="transition-delay:${idx * 50}ms">${letter}</span>`)
        .join('')
})