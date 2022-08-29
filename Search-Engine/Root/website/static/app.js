(function () {
  'use strict';
  angular
  .module('selectDemoBasic', ['ngMaterial','ngAnimate', 'ui.bootstrap'], function($interpolateProvider){
    $interpolateProvider.startSymbol("[[");
    $interpolateProvider.endSymbol("]]");
  })
  .controller('AppCtrl', function($scope, $http, $location) {
    var ctrl = this;

    ctrl.searchWord = ''
    ctrl.displayResults = '';
    ctrl.results = [];
    ctrl.actualResults = [];

    $scope.myInterval = 0;
    $scope.noWrapSlides = false;
    $scope.active = 0;
    var slides = $scope.slides = [];
    var currIndex = 0;
    ctrl.loadingData = true;
    ctrl.showCarousel = false;

    ctrl.displayOptions = ('Default,Top 5,Top 10,All').split(',').map(function (num) { return { abbrev: num }; });
    
    function create_UUID(){
      var dt = new Date().getTime();
      var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
          var r = (dt + Math.random()*16)%16 | 0;
          dt = Math.floor(dt/16);
          return (c=='x' ? r :(r&0x3|0x8)).toString(16);
      });
      return uuid;
    }

    ctrl.corrections = function(ctrl) {
      if (typeof(Storage) !== "undefined") {
        // Store
        var uuid = create_UUID();
        localStorage.setItem(uuid, JSON.stringify(ctrl.actualResults));
        // Retrieve
        window.location = location.href + "annotate/" + uuid;
      } else {
        alert("Sorry, your browser does not support Web Storage.");
      }
    }

    ctrl.getData = function(ctrl){
      slides = $scope.slides = [];
      ctrl.searchWord = angular.copy(ctrl.searchWord);
      ctrl.displayResults = angular.copy(ctrl.displayResults);
      ctrl.loadingData = true;
      ctrl.showCarousel = true;

      $http({
              method: 'POST',
              url: location.href + 'search',
              headers: {
                 'Content-Type': 'application/json;charset=utf-8'
              },
              data: {
                word: ctrl.searchWord,
                display: ctrl.displayResults
              }
          })
          .then(function(resp){
            console.log(resp);
            ctrl.results = resp.data.data;
            ctrl.actualResults = resp.data.actualData;
            ctrl.loadingData = false;
            $scope.addSlides();
          },function(error){
              console.log(error);
          });
    }

    $scope.addSlides = function() {
      currIndex = 0;
      if (ctrl.results.length === 0) {
        document.getElementById('correct').disabled = true;
        alert("Nothing to show!");
      }
      else {
        for (var i = 0, l = ctrl.results.length; i < l; i++) {
          slides.push({
            image: ctrl.results[i].page,
            id: currIndex++,
            path: ctrl.results[i].path
          });
        }
        document.getElementById('correct').disabled = false;
      }
    };

    ctrl.zoomImage = function(id, z){
      var imgId = document.getElementById("img"+id);
      if(z){        
        imgId.onmousemove = function(e){
          var x = e.clientX - 425;
          var y = e.clientY - 250;
          //img1.css({'-webkit-transform-origin-x': x+'px', '-webkit-transform-origin-y':y+'px', '-webkit-transform': 'scale(2)', '-ms-transform':'scale(2)'});
          imgId.style.cssText = '-webkit-transform-origin-x:'+ x +'px;' + '-webkit-transform-origin-y:' + y +'px;' + '-webkit-transform: scale(2);' + '-ms-transform:scale(2);';
        };
      }
      else{
        imgId.style.cssText = '-webkit-transform: scale(1);' + '-ms-transform:scale(1);';
      }
    }
    
    function findScreenCoords(mouseEvent)
    {
      var xpos;
      var ypos;
      console.log('coord');
      console.log(mouseEvent);

      app.controller('ModalInstanceCtrl', function ($scope, $modalInstance, items) {

        $scope.items = items;
        $scope.selected = {
          item: $scope.items[0]
        };
      
        $scope.ok = function () {
          $modalInstance.close($scope.selected.item);
        };
      
        $scope.cancel = function () {
          $modalInstance.dismiss('cancel');
        };
      });
    }
  });
})();
