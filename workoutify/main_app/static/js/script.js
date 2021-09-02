let m = new Array();
m[0] = "Jan.";
m[1] = "Feb.";
m[2] = "March";
m[3] = "April";
m[4] = "May.";
m[5] = "June";
m[6] = "July";
m[7] = "Aug.";
m[8] = "Sept.";
m[9] = "Oct.";
m[10] = "Nov.";
m[11] = "Dec.";

$(document).ready(function () {

    let csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $('#add-sched-workout-btn').click(function () {

        
        let serializedData = $("#scheduleFormAdd").serialize();

        $.ajax({
            url: $("#scheduleFormAdd").data('url'),
            data: serializedData,
            type: 'post',
            success: function(response) {
                let dateString = response.schedule.date
                let time = response.schedule.time;
                let hours = parseInt(time.slice(0, time.indexOf(':')));
                let suffix = ""
                if (hours < 12 && hours > 0){
                    suffix = "a.m.";
                } else if (hours == 0) { 
                    hours = 12;
                    suffix = "a.m.";
                } else if (hours == 12) {
                    suffix = "p.m.";
                } else {
                    hours -= 12;
                    suffix = "p.m.";
                }
                let minutes = time.slice(time.indexOf(':'), getPosition(time, ':', 2));
                let formattedTime = `${hours}${minutes} ${suffix}`

                let month = m[parseInt(dateString.slice(5, 7)) - 1];
                let day = parseInt(dateString.slice(8, 10)).toString();
                let year = dateString.slice(0, 4);
                
                
                $("#scheduleTable").prepend(`<tr id="schedRow" data-id="${response.schedule.id}">
                <td>${month} ${day}, ${year}</td>
                <td>${formattedTime}</td>
                <td>
                <button id="scheduleRemove" type="submit" class="btn" data-id="${response.schedule.id}">
                <i class="material-icons">close</i>
                </button>
                </td></tr>`)
            }
        })
        $("#scheduleFormAdd")[0].reset();

    });

    $('#scheduleTable').on('click', 'button#scheduleRemove', function(event) {

        let scheduleId = $(this).data('id');
        let workoutId = $('#workout').data('id');

        $.ajax({
            url: `/workouts/${workoutId}/delete_schedule/${scheduleId}/`,
            data: {
                csrfmiddlewaretoken: csrfToken,
                schedule_id: scheduleId,
                workout_id: workoutId
            },
            type: 'post',
            dataType: 'json',
            success: function() {
                $(`#schedRow[data-id="${scheduleId}"]`).remove();
            }
        })
    })

    $('#availableExercises').on('click','button#exerciseAdd', function () {

        let exerciseId = $(this).data('id');
        let workoutId = $('#workout').data('id');

        $.ajax({
            url: `/workouts/${workoutId}/assoc_exercise/${exerciseId}/`,
            data: {
                csrfmiddlewaretoken: csrfToken,
                exercise_id: exerciseId,
                workout_id: workoutId
            },
            type: 'post',
            success: function(response) {

                $("#currentExercises").append(
                    `<li data-id="${ response.exercise.id }">
                        <div class="card">
                            <div class="card-content">
                                <span class="card-title activator grey-text text-darken-4">
                                    ${ response.exercise.name }<i class="material-icons right">more_vert</i>
                                </span>
                                <p>${ response.exercise.sets } Sets</p>
                                <p>${ response.exercise.reps } Reps</p>
                            </div>
                        
                            <div class="card-reveal">
                                <span class="card-title grey-text text-darken-4">${ response.exercise.name }<i class="material-icons right">close</i></span>
                                <p>${ response.exercise.description }</p>
                                <p>${ response.exercise.sets } Sets</p>
                                <p>${ response.exercise.reps } Reps</p>
                            </div>
                            <div class="card-action">
                                <button id="exerciseRemove" type="submit" class='btn' data-id="${ response.exercise.id }">Remove From Workout</button>
                            </div>
                        </div>
                    </li>`)

                $(`#availableExercises li[data-id="${ response.exercise.id }"]`).remove();

                if (!(document.querySelectorAll("#availableExercises li").length)){
                    $('#availableExercises').prepend('<h5 id="allExercisesText">All Exercises have been added to the workout</h5>')
                }

                $('#noExercisesText').remove();
                
            }
            
        })
    });

    $('#currentExercises').on('click', 'button#exerciseRemove', function () {

        let exerciseId = $(this).data('id');
        let workoutId = $('#workout').data('id');


        $.ajax({
            url: `/workouts/${workoutId}/unassoc_exercise/${exerciseId}/`,
            data: {
                csrfmiddlewaretoken: csrfToken,
                exercise_id: exerciseId,
                workout_id: workoutId
            },
            type: 'post',
            success: function(response) {              
                
                
                $("#availableExercises").append(
                    `<li data-id="${ response.exercise.id }">
                        <div class="card">
                            <div class="card-content">
                                <span class="card-title activator grey-text text-darken-4">
                                    ${ response.exercise.name }<i class="material-icons right">more_vert</i>
                                </span>
                                <p>${ response.exercise.sets } Sets</p>
                                <p>${ response.exercise.reps } Reps</p>
                            </div>
                            
                            <div class="card-reveal">
                                <span class="card-title grey-text text-darken-4">${ response.exercise.name }<i class="material-icons right">close</i></span>
                                <p>${ response.exercise.description }</p>
                                <p>${ response.exercise.sets } Sets</p>
                                <p>${ response.exercise.reps } Reps</p>
                            </div>
                            <div class="card-action">
                                <button id="exerciseAdd" type="submit" class='btn' data-id="${ response.exercise.id }">Add To Workout</button>
                            </div>
                        </div>
                    </li>`);
                
                $(`#currentExercises li[data-id="${ response.exercise.id }"]`).remove();


                if (!((document.querySelectorAll("#currentExercises li")).length)){
                    $('#currentExercises').prepend('<h5 id="noExercisesText">No Exercises :(</h5>')
                } 

                $('#allExercisesText').remove();
                
            }
        })
    });
})


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


let schedWorkoutBtn = document.getElementById('add-sched-workout-btn');
if (schedWorkoutBtn) {
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
}
function getPosition(string, subString, index) {
    return string.split(subString, index).join(subString).length;
  }

