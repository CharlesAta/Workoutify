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
twelveHour: false
});

let schedWorkoutBtn = document.getElementById('sched-workout-btn');

schedWorkoutBtn.addEventListener('click', function() {
    let time = timeEl.value;
    let hours = parseInt(time.slice(0, time.indexOf(':')));
    if (time.endsWith("AM")){
        if (hours === 12){
            hours = 0;
        }
    } else {
        if (hours < 12){
            hours += 12;
        }
    }
    let minutes = time.slice(time.indexOf(':'), time.indexOf(' '));
    let two_four_clock = `${hours}${minutes}`
    timeEl.value = two_four_clock;
})
