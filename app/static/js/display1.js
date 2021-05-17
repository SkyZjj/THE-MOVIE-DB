window.onload = function () {
    const homeTab = this.document.getElementById("homeTab");
    const searchTab = this.document.getElementById("searchTab");
    const display1 = this.document.getElementById("display1");
    const display2 = this.document.getElementById("display2");
    const showAll = document.getElementById("showAll");
    const searchForm = document.getElementById("searchForm");
    const Url = searchForm.action;
    searchTab.onclick = function () {
        this.style = "color:red;border-bottom: 1px solid #ddd";
        display2.style.display = "block";
        display1.style.display = "none";
        homeTab.style = "color:white;border-bottom: 0px;";
    };
    homeTab.onclick = function () {
        this.style = "color:red;border-bottom: 1px solid #ddd";
        display1.style.display = "block";
        display2.style.display = "none";
        searchTab.style = "color:white;border-bottom: 0px";
    };

    var box1 = this.document.getElementsByClassName("slideshow")[0];
    var box2 = this.document.getElementsByClassName("slideshow")[1];
    var lik1 = box1.getElementsByTagName("li");
    var lik2 = box2.getElementsByTagName("li");

    function fun(i, j) {
        lik1[i].style.opacity = 1;
        lik1[j].style.opacity = 0;
        lik2[i].style.opacity = 1;
        lik2[j].style.opacity = 0;
    }

    fun(0, 1);
    var i = 0;

    function auto() {
        if (++i >= 5) {
            i = 0;
            fun(0, 4);
        } else fun(i, i - 1);
    }

    timer = this.setInterval(auto, 2000);
    document.getElementById("submitButton").onclick = async function checknull() {
        var keywordInput = document.getElementById("keywordInput").value;
        var categoryInput = document.getElementById("categoryInput").value;
        if (keywordInput == "" || categoryInput == "null") {
            alert("Please enter vaild values.");
            return;
        }

        var searchUrl = Url + '/search';
        // alert(searchUrl);
        // var searchUrl = 'http://127.0.0.1:5000/search';
        // alert(searchUrl);
        var url = '/search?keywordInput=' + keywordInput + '&categoryInput=' + categoryInput;
        // alert(url);
        const response = await fetch(url, {
            method: 'GET',
            mode: 'cors'
        });
        // alert(response)
        let showText = await response.text();
        // console(showJson)
        // alert(showText);
        var showJson = JSON.parse(showText);
        // alert(showJson.result[0].id);

        create_e = function (tag_, class_) {
            var elem = document.createElement(tag_);
            elem.setAttribute('class', class_);
            return elem;
        }
        var showData = showJson.result;
        // var html = '';
        showAll.innerHTML='';
        if (showData.length == 0) {
            // html += '<div id="noResult">No results found.</div>';
            var noResult = document.createElement('div');
            noResult.setAttribute('id', 'noResult');
            noResult.innerHTML = 'No results found.';
            showAll.appendChild(noResult);

            // alert(html)
        } else {
            // html += '<div id="showResults">Showing results...</div>';
            var showResults = document.createElement('div');
            showResults.setAttribute('id', 'showResults');
            showResults.innerHTML = 'Showing results...';
            showAll.appendChild(showResults);
            for (var i = 0; i < showData.length; i++) {
                // html += '<div class="show">';
                var show = create_e('div', 'show');

                var redbox = create_e('div', 'redbox');
                // show.appendChild(redbox);
                var imgshow = document.createElement('img');
                imgshow.setAttribute('src', showData[i].poster_path);
                show.appendChild(imgshow);
                // html += '<div class="redbox"></div>';
                // html += '<img src="' + showData[i].poster_path + '">';
                var showInfo = create_e('div', 'showInfo');
                // html += '<div class="showInfo">';
                var showTitle = create_e('div', 'showTitle');
                // html += '<div class="showTitle">';
                showTitle.innerHTML = showData[i].name;
                showInfo.appendChild(showTitle);
                // html += showData[i].name;
                // html += '</div>';
                var showDateType = create_e('div', 'showDateType');
                // html += '<div class="showDateType">';
                showDateType.innerHTML = showData[i].date_genre;

                // html += showData[i].date_genre;
                // html += '</div>';
                var catego = showData[i].catego;
                var showRateVote = create_e('div', 'showRateVote');
                var showRate = create_e('div', 'showRate');
                showRate.innerHTML = '&#9733;' + showData[i].vote_average;
                var showVote = create_e('div', 'showVote');
                showVote.innerHTML = showData[i].vote_count;
                showRateVote.appendChild(showRate);
                showRateVote.appendChild(showVote);
                showInfo.appendChild(showRateVote);
                // html += '<div class="showRateVote">';
                // html += '<div class="showRate">';
                // html += '&#9733;' + showData[i].vote_average;
                // html += '</div>';
                // html += '<div class="showVote">';
                // html += showData[i].vote_count;
                // html += '</div>';
                // html += '</div>';
                // html += '<div class="showIntro">' + showData[i].overview;
                // html += '</div>';
                var showIntro = create_e('div', 'showIntro');
                showIntro.innerHTML = showData[i].overview;
                showInfo.appendChild(showIntro);
                var showmorebutton = create_e('button', 'showMore');
                showmorebutton.setAttribute('id', showData[i].id);
                showmorebutton.setAttribute('catego', catego);
                // console(showData[i].overview);
                showmorebutton.innerHTML = 'Show more';
                showmorebutton.addEventListener('click', function (e) {
                    var button_id = e.target.getAttribute('id');
                    var button_category = e.target.getAttribute('catego');

                    showMoreFun(button_category, button_id);
                })
                showInfo.appendChild(showmorebutton);
                // html += '<button class="showMore" name="' + showData[i].id +'" value="' + showData[i].catego + '" > Show more</button>';
                // html += '</div>';
                // html += '</div>';
                show.appendChild(showInfo);
                showAll.appendChild(show);
            }

        }


    }
    document.getElementById("clearButton").onclick = function () {
        showAll.innerHTML = '';
    }

    showMoreFun = async function (category_, id_) {
        // alert("in");
        var showUrl = '/show?category=' + category_ + '&id=' + id_;
        // alert('ok');
        var showResponse = await fetch(showUrl, {
            method: 'GET',
            mode: 'cors'
        });
        // console(showJson)
        // alert(showText);
        var result_html = await showResponse.text();
        // alert(result_html);
        popDiv.innerHTML = result_html
        // '<div id=closePop onclick="closePop()">&#10006;</div>'
        var closePop =document.createElement('div');
        closePop.setAttribute('id','closePop');
        closePop.innerHTML='&#10006;';
        popDiv.appendChild(closePop);
//         var eElement; // some E DOM instance
// var newFirstElement; //element which should be first in E

popDiv.insertBefore(closePop, popDiv.firstChild);
        closePop.onclick=function closePop(){
         popDiv.style.display = "none";
         cover.style.display="none";
        }

        popDiv.style.display = "block";
        cover.style.display = "block";
        // return 'success';
    }
    const popDiv = document.getElementById("popDiv");
    const cover = document.getElementById("cover");
// showmorebutton


//     // alert(showmores)
// var searchForm = document.getElementById("searchForm");
// var Url = searchForm.action;
// alert(Url)





};

