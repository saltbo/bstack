Feature: Notes

  Scenario: notes-add-a-note
    Given I am on the notes page
    When I add a note with surrounding spaces
    Then the note appears in the list without them

  Scenario: notes-refuse-an-empty-note
    Given I am on the notes page
    When I try to add a note with no text, or with more than 500 characters
    Then no note is added

  Scenario: notes-list-newest-first
    Given I have added two notes
    When I look at the list
    Then the newer note comes first
