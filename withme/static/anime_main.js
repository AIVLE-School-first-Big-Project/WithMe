
let pushMessagehide = anime({
    targets: '#pushmessgecontainer',
    translateY: ['0px', '-260px'],
    duration: 1000,
    autoplay: false,
    begin: function() {
    },
});

let pushMessageShow = anime({
    targets: '#pushmessgecontainer',
    translateY: ['-260px', '20px'],
    duration: 500,
    autoplay: false,
    begin: function() {
    },
});


function push_message(text){
    document.querySelector('#push_text').textContent = text
    console.log(text)
    pushMessageShow.play()
};

document.querySelector('#pushconfirm').onclick = (e)=> {
    pushMessagehide.play()
};
