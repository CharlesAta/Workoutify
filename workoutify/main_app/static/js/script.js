  // create a datepicker
let dateEl = document.getElementById('id_date');
M.Datepicker.init(dateEl, {
format: 'yyyy-mm-dd',
defaultDate: new Date(),
setDefaultDate: true,
autoClose: true
});

let timeEl = document.getElementById('id_time');
M.Timepicker.init(timeEl, {
defaultTime: 'now',
});

let schedWorkoutBtn = document.getElementById('sched-workout-btn');

schedWorkoutBtn.addEventListener('click', function() {
    let time = timeEl.value;
    if (time.endsWith("AM")){
        timeEl.value = time.slice(0, 5);
    } else {
        hours = parseInt(time.slice(0, time.indexOf(':')));
        if (hours === 12){
            hours = 0;
        } else {
            hours += 12;
        }
        minutes = time.slice(time.indexOf(':'), time.indexOf(' '));
        two_four_clock = `${hours}${minutes}`
        timeEl.value = two_four_clock;
    }
})
