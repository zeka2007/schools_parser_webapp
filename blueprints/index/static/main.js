const tg = window.Telegram.WebApp;
const average_mark = document.getElementById('average-mark-id');
const most_common_mark = document.getElementById('most-common-mark');
const marks_count = document.getElementById('marks-count');
const best_lesson = document.getElementById('best-lesson');
const best_lesson_average = document.getElementById('best-lesson-average-mark');
const loading_screen = document.getElementById('preloader');

var xhr = new XMLHttpRequest();
xhr.open("GET",
    window.location.protocol + '//' + window.location.host + '/api/get-user-data?' + tg.initData, 
    true);

function setElementColor(element, mark) {
    let set_class = 'mark-green';
    if (mark <= 6 && mark >= 4) set_class = 'mark-purpure';
    if (mark < 4) set_class = 'mark-red';
    element.classList.add(set_class);
}
xhr.onload = () => {
    if (xhr.readyState == 4) {
        if (xhr.status == 200) {
            const data = JSON.parse(xhr.responseText);
            average_mark.textContent = data.average_mark;
            marks_count.textContent = data.marks_count;
            best_lesson.textContent = data.best_lesson.lesson;
            best_lesson_average.textContent = data.best_lesson.average_mark;

            most_common_mark.textContent = data.most_common;
            setElementColor(most_common_mark, data.most_common)
            setElementColor(best_lesson_average, data.best_lesson.average_mark)

            if (!loading_screen.classList.contains('done')) {
                loading_screen.classList.add('done');
            }
        }
    }
};
xhr.send();