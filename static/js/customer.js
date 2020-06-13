
$('.nav-link').click(function() {
    let complete = this.dataset['complete']
    let list_true = document.querySelectorAll('.card-body .True')
    let list_false = document.querySelectorAll('.card-body .False')
    console.log(complete)
    $('.nav-link').not(this).each(function(){
        $(this).removeClass('active');
    })
    $(this).addClass('active');

    if (complete=='false') {
        for (var i = 0; i < list_true.length; ++i) {
            list_true[i].classList.add('hide');
         }
         for (var i = 0; i < list_false.length; ++i) {
            list_false[i].classList.remove('hide');
         }
    } else {
        for (var i = 0; i < list_true.length; ++i) {
            list_true[i].classList.remove('hide');
         }
        for (var i = 0; i < list_false.length; ++i) {
            list_false[i].classList.add('hide');
         }
    }
    
})
