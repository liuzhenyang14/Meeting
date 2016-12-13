'use strict';

var appCtrl = angular.module('ConfPlusWebApp.controllers', []);

appCtrl.controller('MainController', function($rootScope, $scope, $routeParams){

  $scope.swiped = function(direction) {
    alert('Swiped ' + direction);
  };

  // User agent displayed in home page
  $scope.userAgent = navigator.userAgent;
  
  // Needed for the loading screen
  $rootScope.$on('$routeChangeStart', function(){
    $rootScope.loading = true;
  });

  $rootScope.$on('$routeChangeSuccess', function(){
    $rootScope.loading = false;
  });

  $rootScope.url = serverUrlHead;
  //$rootScope.menus;
  $rootScope.userId = '-1';
  $rootScope.errMsg = '';
  
});

//confInfo
appCtrl.controller('confInfoCtrl', ['$scope', '$rootScope', '$sce', '$routeParams', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $sce, $routeParams, getConfInfo, getMenuList) {
	console.log('confInfoCtrl: confId=' + $routeParams.confId);
	
	$rootScope.confId = $routeParams.confId;
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});	
}]);

//Login
appCtrl.controller('loginCtrl', ['$scope', '$rootScope', 'login', function ($scope, $rootScope, login){
	
	$scope.login = function(){
		console.log('loginCtrl:login:  userEmail=' + $scope.userEmail + ', userPassword=' + $scope.userPassword);
		login.login($scope.userEmail, $scope.userPassword, $rootScope);
		if($rootScope.userId == "-1"){
			$rootScope.errMsg = 'Cannot find your registration information, please try again or contact organizer.';
		}
	}
	
	$scope.logout = function(){
		console.log('loginCtrl:logout');
		$rootScope.userId = "0";
	}
	
}]);

//Session List
appCtrl.controller('sessionListCtrl', ['$scope', '$rootScope', '$routeParams', 'getSessDates', 'getSessList', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $routeParams, getSessDates, getSessList, getConfInfo, getMenuList) {
	console.log('sessionListCtrl:  confId=' + $routeParams.confId + ', title=' + $routeParams.title + ', type=' + $routeParams.type + ', userId=' + $rootScope.userId);

	$scope.i = 0;
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;	
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	
	//read dates from server
	$scope.sessionDates = getSessDates.query({confId: $rootScope.confId, type: $routeParams.type});
	//read session list from server
	$scope.sessions = getSessList.query({confId: $rootScope.confId, type: $routeParams.type, userId:$rootScope.userId});

	//is the current show date
	$scope.isShowDate = function(i,sessionDate){
        var flag = false;
        if(!sessionDate || $scope.sessionDates[i].showDate === sessionDate.showDate){
            flag = true;
        }
		console.log('isShowDate: i=' + i + ' sessionDate=' + sessionDate.showDate + ' flag=' + flag);
        return flag;
    }
	
	//is Session in this Date
	$scope.isShowSession = function(i,session){
        var flag = false;
        if(!session || $scope.sessionDates[i].showDate === session.showDate){
            flag = true;
        }
		console.log('isShowSession: i=' + i + ' $scope.sessionDates[i]=' + $scope.sessionDates[i].showDate + ' session.showDate=' + session.showDate + ' flag=' + flag);
        return flag;
    }
	
	//is in range of Dates Array
	$scope.inArray = function(i){
		console.log('inArray: i=' + i);
		var flag = false;
        if(i < $scope.sessionDates.length - 1){
            flag = true;
        }
        return flag;
	}
}]);

//Session Detail
appCtrl.controller('sessionDetailCtrl', ['$scope', '$rootScope', '$sce', '$routeParams', 'getSessDetail', 'getConfInfo', 'saveSchedule', 'getMenuList', function ($scope, $rootScope, $sce, $routeParams, getSessDetail, getConfInfo, saveSchedule, getMenuList) {
	console.log('sessionDetailCtrl: title=' + $routeParams.title + ', sessId=' + $routeParams.sessId + ', userId=' + $rootScope.userId);
	
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;
	$scope.res = '-1';
	$scope.resMsg = '';
	$scope.errMsg = '';
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});

	//read session detail from server
	$scope.session = getSessDetail.get({sessId: $routeParams.sessId, userId:$rootScope.userId});
	
	//is there members in this session
	$scope.hasMember = function(){
		console.log('hasMember()');
		var flag = false;
        if($scope.session.memberlist!=null && $scope.session.memberlist !=""){
            flag = true;
        }
        return flag;
	};
	
	$scope.join = function(){
		console.log('sessionDetailCtrl:join(sessId:' + $routeParams.sessId + ',userId:' +$rootScope.userId + ",attend:"+ '1)')

		if($rootScope.userId == null || $rootScope.userId == 0 || $rootScope.userId == -1){
			$scope.errMsg = 'Please login at side sliding menu to register for any session.';
			$scope.resMsg = '';
		}else{
			saveSchedule.save($routeParams.sessId, $rootScope.userId, '1', $scope);
		}
		
	};
	
	$scope.cancel = function(){
		console.log('sessionDetailCtrl:cancel(sessId:' + $routeParams.sessId + ',userId:' +$rootScope.userId + ",attend:"+ '0)');
		if($rootScope.userId == null || $rootScope.userId == 0 || $rootScope.userId == -1){
			$scope.errMsg = 'Please login at side sliding menu to register for any session.';
			$scope.resMsg = '';
		}else{
			saveSchedule.save($routeParams.sessId, $rootScope.userId, '0', $scope);
			$scope.session.attend == '0';
		}
	};
	
}]);

//Member list
appCtrl.controller('memberListCtrl', ['$scope', '$rootScope', '$routeParams', 'getMemberList', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $routeParams, getMemberList, getConfInfo, getMenuList) {
	console.log('memberListCtrl:  confId=' + $routeParams.confId + ', title=' + $routeParams.title + ', type=' + $routeParams.type);
	
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;	
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	
	$scope.members = getMemberList.query({confId: $rootScope.confId, type: $routeParams.type});
}]);


//Member Detail
appCtrl.controller('memberDetailCtrl', ['$scope', '$rootScope', '$sce', '$routeParams', 'getMemDetail', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $sce, $routeParams, getMemDetail, getConfInfo, getMenuList) {
	console.log('memberDetailCtrl: title=' + $routeParams.title + ', memId=' + $routeParams.memId);
	
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;	
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	
	$scope.member = getMemDetail.get({memId: $routeParams.memId});
	
	//is there sessions for this member
	$scope.hasSession = function(){
		console.log('hasSession()');
		var flag = false;
        if($scope.member.sessList!=null && $scope.member.sessList !=""){
            flag = true;
        }
        return flag;
	}
}]);

//Company list
appCtrl.controller('cmpListCtrl', ['$scope', '$rootScope', '$routeParams', 'getCmpList', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $routeParams, getCmpList, getConfInfo, getMenuList) {
	console.log('cmpListCtrl:  confId=' + $routeParams.confId + ', title=' + $routeParams.title + ', type=' + $routeParams.type);
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;	
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	
	$scope.companys = getCmpList.query({confId: $rootScope.confId, type: $routeParams.type});
	
}]);

//Company Detail
appCtrl.controller('cmpDetailCtrl', ['$scope', '$rootScope', '$sce', '$routeParams', 'getCmpDetail', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $sce, $routeParams, getCmpDetail, getConfInfo, getMenuList) {
	console.log('cmpDetailCtrl: title=' + $routeParams.title + ', cmpId=' + $routeParams.cmpId);
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;	
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	
	$scope.company = getCmpDetail.get({cmpId: $routeParams.cmpId});
}]);

//Map list
appCtrl.controller('mapListCtrl', ['$scope', '$rootScope', '$routeParams', 'getMapList', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $routeParams, getMapList, getConfInfo, getMenuList) {
	console.log('mapListCtrl:  confId=' + $routeParams.confId + ', title=' + $routeParams.title);
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;	
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	
	$scope.maps = getMapList.query({confId: $rootScope.confId});
	
}]);

//Map Detail
appCtrl.controller('mapDetailCtrl', ['$scope', '$rootScope', '$sce', '$routeParams', 'getMapDetail', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $sce, $routeParams, getMapDetail, getConfInfo, getMenuList) {
	console.log('mapDetailCtrl: title=' + $routeParams.title + ', mapId=' + $routeParams.mapId);
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;	
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	
	$scope.map = getMapDetail.get({mapId: $routeParams.mapId});
}]);

//Custom list
appCtrl.controller('customListCtrl', ['$scope', '$rootScope', '$routeParams', 'getCustomList', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $routeParams, getCustomList, getConfInfo, getMenuList) {
	console.log('customListCtrl:  confId=' + $routeParams.confId + ', title=' + $routeParams.title + ', type=' + $routeParams.type);
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	
	$scope.customs = getCustomList.query({confId: $rootScope.confId, type: $routeParams.type});
	
}]);

//Custom Info Detail
appCtrl.controller('customDetailCtrl', ['$scope', '$rootScope', '$sce', '$routeParams', 'getCustomDetail', 'getConfInfo', 'getMenuList', function ($scope, $rootScope, $sce, $routeParams, getCustomDetail, getConfInfo, getMenuList) {
	console.log('customDetailCtrl: title=' + $routeParams.title + ', customId=' + $routeParams.customId);
	$rootScope.title = $routeParams.title;
	$rootScope.confId = $routeParams.confId;	
	$rootScope.confInfo = getConfInfo.get({confId: $rootScope.confId});
	$rootScope.menus = getMenuList.query({confId: $rootScope.confId});
	
	$scope.custom = getCustomDetail.get({customId: $routeParams.customId});
}]);