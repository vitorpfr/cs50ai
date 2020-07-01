1. If Hermione is in the library, then Harry is in the library. (HermioneLibrary -> HarryLibrary)
2. Hermione is in the library.                                  (HermioneLibrary)
3. Ron is in the library and Ron is not in the library.         (RonLibrary ^ ¬RonLibrary)
4. Harry is in the library.                                     (HarryLibrary)
5. Harry is not in the library or Hermione is in the library.   (¬HarryLibrary v HermioneLibrary)
6. Ron is in the library or Hermione is in the library.         (RonLibrary v HermioneLibrary)

Which of the following logical entailments is true? *
1 point
entail: "In every model in which sentence alpha is true, sentence beta is also true"
Sentence 1 entails Sentence 4: strong no
Sentence 6 entails Sentence 3: strong no
Sentence 2 entails Sentence 5: yes
Sentence 1 entails Sentence 2: no
Sentence 5 entails Sentence 6: no
Sentence 6 entails Sentence 2: no

Sentence 1 is true when
HermioneLibrary is true and HarryLibrary is true -> 4 is true
HermioneLibrary is false (doesn't matter HarryLibrary) -> 4 may be false

Sentence 6 is true when:
RonLibrary is true -> 3 is false
HermioneLibrary is true
Both are true

Sentence 2 is true when:
HermioneLibrary is true -> 5 is true

Sentence 1 is true when
HermioneLibrary is true and HarryLibrary is true -> 2 is true
HermioneLibrary is false (doesn't matter HarryLibrary) -> 2 is false

Sentence 5 is true when:
HarryLibrary is false -> 6 may be false
HermioneLibrary is true -> 6 is true

Sentence 6 is true when:
RonLibrary is true -> 2 may be false
HermioneLibrary is true -> 2 is true

Answer: Sentence 2 entails Sentence 5

Exclusive or:

(A v B) ^ not(A ^ B)

Answer: (A ∨ B) ∧ ¬ (A ∧ B)

R: It is raining
C: It is cloudy
S: It is sunny

If it is raining, then it is cloudy and not sunny

R -> (C ^ ¬S)


Student(x): "x is a student"

Course(x): "x is a course"

Enrolled(x,y): "x is enrolled in y"

There is a course that Harry and Hermione are both enrolled in

ThereExistsA x that Course(x) ^ Enrolled(Harry,x) ^ Enrolled(Hermione,x)

Answer: ∀x. Course(x) ∧ Enrolled(Harry, x) ∧ Enrolled(Hermione, x)
