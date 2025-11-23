(function(){
    var form = document.getElementById('botSearchForm');
    var input = document.getElementById('botSearch');
    var btn = document.getElementById('botSearchBtn');
    var msg = document.getElementById('botMessage');

    var botsSet = null;
    var fetchDone = false;
    var fetchFailed = false;

    function showMessage(text, isError){
        msg.textContent = text;
        msg.className = isError ? 'w3-text-red w3-margin-top' : 'w3-text-green w3-margin-top';
    }

    fetch('/available_bots.txt')
        .then(function(res){
            if(!res.ok) throw new Error('Network response was not ok');
            return res.text();
        })
        .then(function(text){
            var lines = text.split(/\r?\n/).map(function(l){ return l.trim(); }).filter(Boolean);
            var s = new Set();
            lines.forEach(function(l){ s.add(l.toLowerCase()); });
            botsSet = s;
        })
        .catch(function(err){
            console.error('Could not load available_bots.txt', err);
            fetchFailed = true;
            showMessage('Warning: could not verify database. Please try again later.', true);
        })
        .finally(function(){
            fetchDone = true;
        });

    function doSearch(){
        var name = input.value.trim();
        if(!name){
            input.focus();
            showMessage('Please enter a bot name.', true);
            return;
        }

        if(!fetchDone){
            showMessage('Still verifying database—please wait a moment.', true);
            return;
        }

        if(fetchFailed){
            showMessage('Sorry. Could not verify the database right now. Please try again later.', true);
            return;
        }

        if(botsSet && botsSet.has(name.toLowerCase())){
            var TYPES = [
                'bullet',
                'blitz',
                'rapid',
                'classical',
                'chess960',
                'antichess',
                'atomic',
                'crazyhouse',
                'horde',
                'kingOfTheHill',
                'racingKings',
                'threeCheck',
                'correspondence',
            ];

            var DISPLAY = {
                'bullet': 'Bullet',
                'blitz': 'Blitz',
                'rapid': 'Rapid',
                'classical': 'Classical',
                'chess960': 'Chess960',
                'antichess': 'Antichess',
                'atomic': 'Atomic',
                'crazyhouse': 'Crazyhouse',
                'horde': 'Horde',
                'kingOfTheHill': 'King of the Hill',
                'racingKings': 'Racing Kings',
                'threeCheck': 'Three Check',
                'correspondence': 'Correspondence'
            };

            function showLoading(){
                msg.className = '';
                msg.innerHTML = '<div class="w3-margin-top"><span class="loader" aria-hidden="true"></span><span class="loader-text">Loading ranks…</span></div>';
                btn.disabled = true;
                input.disabled = true;
            }

            function hideLoading(){
                btn.disabled = false;
                input.disabled = false;
            }

            showLoading();

            var usernameLower = name.toLowerCase();

            function showResults(results){
                msg.className = '';
                msg.innerHTML = '';
                var table = document.createElement('table');
                table.className = 'w3-table w3-striped w3-margin-top';

                var thead = document.createElement('thead');
                var headerRow = document.createElement('tr');
                var thVariant = document.createElement('th');
                thVariant.textContent = 'Variant';
                var thRank = document.createElement('th');
                thRank.textContent = 'Rank';
                headerRow.appendChild(thVariant);
                headerRow.appendChild(thRank);
                thead.appendChild(headerRow);
                table.appendChild(thead);

                var tbody = document.createElement('tbody');
                results.forEach(function(r){
                    var row = document.createElement('tr');
                    var tdVariant = document.createElement('td');
                    tdVariant.textContent = r.display;
                    var tdRank = document.createElement('td');
                    tdRank.textContent = r.rank;
                    row.appendChild(tdVariant);
                    row.appendChild(tdRank);
                    tbody.appendChild(row);
                });
                table.appendChild(tbody);

                msg.appendChild(table);
            }

            (async function(){
                var results = [];
                try{
                    for(var t=0;t<TYPES.length;t++){
                        var type = TYPES[t];
                        var display = DISPLAY[type] || type;
                        var rankText = 'no rank';
                        try{
                            var res = await fetch('/bot_leaderboard/' + type + '.md');
                            if(res.ok){
                                var text = await res.text();
                                var lines = text.split(/\r?\n/);
                                for(var i=0;i<lines.length;i++){
                                    var line = lines[i].trim();
                                    if(!line) continue;
                                    var parts = line.split('|');
                                    if(parts.length >= 2){
                                        var botField = parts[1].replace(/^@/, '').trim().toLowerCase();
                                        if(botField === usernameLower){
                                            var r = parts[0].replace(/^#/, '').trim();
                                            rankText = r || 'no rank';
                                            break;
                                        }
                                    }
                                }
                            }
                        }catch(e){
                            // ignore
                        }
                        results.push({display: display, rank: rankText});
                    }
                }finally{
                    showResults(results);
                    hideLoading();
                }
            })();

        } else {
            showMessage('Sorry. The bot name entered is either invalid or unavailable in our database.', true);
        }
    }

    btn.addEventListener('click', function(e){
        e && e.preventDefault();
        doSearch();
    });

    form.addEventListener('submit', function(e){
        e && e.preventDefault();
        doSearch();
    });
})();
