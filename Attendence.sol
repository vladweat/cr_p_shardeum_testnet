// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract Attendence {
    address teacher = msg.sender;
    uint256 Totalstudent = 20;
    uint256 public Totalstudent_pre = 0;
    uint256 public todaystu;
    mapping(address => bool) public Present_in_class;

    function yesMam(address studentID) public {
        require(!Present_in_class[studentID], "already atended");
        Present_in_class[studentID] = true;
        Totalstudent_pre++;
    }

    function todayaatendence() public {
        todaystu = Totalstudent - Totalstudent_pre;
    }
}
