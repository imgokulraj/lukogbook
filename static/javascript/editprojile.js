document.querySelector('#profile-bio-field').addEventListener('click' , (e) => { 
    e.preventDefault() 
    profileBioForm = document.forms['profilebioform'].submit()
})