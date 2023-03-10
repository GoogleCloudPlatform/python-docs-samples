// Copyright 2016 Google LLC.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

function handleResponse(resp){
  const li = document.createElement('li');
  li.innerHTML = resp;
  document.querySelector('.responses').appendChild(li)
}

function handleClick(event){
  $.ajax({
    url: `hello/${event.target.id}`,
    type: `GET`,
    success(resp){
      handleResponse(resp);
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.getElementsByTagName('button')
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', handleClick);
  }
});
