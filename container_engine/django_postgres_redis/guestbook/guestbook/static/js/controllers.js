/**
 * Copyright (c) 2015 Google Inc.
 * <p/>
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 * <p/>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p/>
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */


var guestbookApp = angular.module('guestbook', ['ui.bootstrap']);


/**
 * Constructor
 */
function GuestbookController() {
}

GuestbookController.prototype.onSubmit = function () {
    this.scope_.messages.push({text: this.scope_.msg});
    this.http_.post('messages/', this.scope_.msg,
        function success() {
            console.log("updated!");
        });
    console.log(this.scope_.messages);
    this.scope_.msg = "";
};

guestbookApp.controller('GuestbookCtrl', function ($scope, $http, $location) {
    $scope.controller = new GuestbookController();
    $scope.controller.scope_ = $scope;
    $scope.controller.location_ = $location;
    $scope.controller.http_ = $http;
    $scope.messages = [];
    $scope.controller.http_.get("messages/")
        .success(function (data) {
            $scope.messages = _.pluck(data, 'fields');
            console.log($scope.messages);
        });
});
