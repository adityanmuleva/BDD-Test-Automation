@All_Test

  Feature: This feature file contains scenarios related to doctor

    @Doctor_login
    Scenario: Login to doctor account
      Given I open operable web Page
      When I login to operable with username "DOCTOR_CONFIG["USERNAME_1"]", password "DOCTOR_CONFIG["PASSWORD_1"]"
#      When I Create Patient
