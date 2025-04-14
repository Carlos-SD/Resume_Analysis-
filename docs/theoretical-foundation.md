
# Theoretical Foundations of the Resume Analysis System

## 1. Introduction to Formal Language Theory

Formal language theory provides a mathematical framework for describing and analyzing textual patterns. In this project, we apply fundamental concepts from this theory to implement an efficient and robust resume analysis system.

## 2. Regular Languages and Regular Expressions

### 2.1 Theoretical Foundations

A regular language is one that can be recognized by a finite automaton or described using a regular expression. In our project, we use regular expressions to identify and extract specific text patterns.

Regular expressions represent search patterns composed of:
- Literal characters  
- Metacharacters (., +, *, ?, etc.)  
- Character classes ([a-z], \d, \w, etc.)  
- Quantifiers and anchors  

### 2.2 Application in the Project

In our system, regular expressions are used to:

1. **Identify resume sections**: Detect titles such as "EDUCATION", "WORK EXPERIENCE".
2. **Extract structured data**: Retrieve personal information such as email, phone number, name.
3. **Detect specific skills**: Identify technologies and competencies relevant to each role.

Implementation example from `regex_config.py`:
```python
email_regex = r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}"
phone_regex = r"(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})"
education_regex = r"EDUCATION\s*\n(.*?)(?=\n[A-Z\s]+(?:\n|$))"
```

## 3. Deterministic Finite Automata (DFA)

### 3.1 Theoretical Foundations

A deterministic finite automaton (DFA) is an abstract machine composed of:
- A finite set of states  
- An input alphabet  
- A transition function  
- An initial state  
- A set of final or accepting states  

A DFA processes an input string symbol by symbol, moving between states according to the defined transitions. If it ends in an accepting state, the string is considered accepted.

### 3.2 Application in the Project

In our system, we implemented a DFA to classify resumes based on the presence or absence of critical components:

1. **States**: Represent stages in the resume evaluation process.
2. **Alphabet**: Symbols that represent the presence (`name`, `email`, etc.) or absence (`missing_name`, `missing_email`, etc.) of information.
3. **Final states**: Represent classifications such as "HIGHLY QUALIFIED", "NEEDS REVIEW", or "REJECTED".

Implementation in `resume_classifier.py`:
```python
self.dfa = DeterministicFiniteAutomaton(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9'},
    input_symbols=self.alphabet,
    start_state='q0',
    final_states={'q7', 'q8', 'q9'}
)
```

## 4. Finite State Transducers (FST)

### 4.1 Theoretical Foundations

A finite state transducer (FST) is an extension of a finite automaton that not only recognizes strings but also produces output. An FST can be seen as a device that converts between two regular languages.

Formally, an FST includes:
- A finite set of states  
- An input alphabet  
- An output alphabet  
- A transition function mapping states to input-output pairs  
- An initial state  
- A set of final states  

### 4.2 Application in the Project

In our system, we use a simplified FST to evaluate and transform work experience information:

1. **States**: Represent experience levels (entry, mid, senior).
2. **Inputs**: Keywords and years of experience.
3. **Outputs**: Numerical scores reflecting relevance and level.

Implementation in `resume_ranker.py`:
```python
self.experience_fst_states = {
    'start': {'junior': ('mid', 0.5), 'intern': ('entry', 0.3), 'senior': ('senior', 1.0), '': ('entry', 0.3)},
    # ...
}
```

This FST allows us to not only recognize patterns but also assign them quantitative values.

## 5. Context-Free Grammars (CFG)

### 5.1 Theoretical Foundations

A context-free grammar (CFG) is a formal system that describes a language through a set of production rules. A CFG consists of:
- A set of non-terminal symbols  
- A set of terminal symbols  
- A set of production rules  
- A start symbol  

Unlike regular languages, CFGs can express nested and recursive structures.

### 5.2 Application in the Project

In our system, we use the `textx` library to define a grammar that validates the structure of resume summaries:

```
ResumeSummary:
    personal_info=PersonalInfo
    summary=Summary
;

PersonalInfo:
    'Personal Information:'
    full_name=/.+/
    email=/.+/
    phone=/.+/
    location=/.+/
    linkedin=/.+/
    portfolio=/.+/
;

Summary:
    'Summary:'
    content=/.+/
;
```

This grammar allows us to:
1. **Validate structure**: Ensure the information follows a predefined format.
2. **Detect inconsistencies**: Identify missing or poorly formatted data.
3. **Generate visualizations**: Transform information into formats like HTML or Markdown.

## 6. Integration of Concepts

The power of our system lies in the combination of these theoretical concepts:

1. **Regular Expressions** for initial data extraction.
2. **DFA** for binary candidate classification.
3. **FST** for assigning quantitative scores.
4. **CFG** for structural validation and summary generation.

This integration allows us to address different aspects of natural language processing:
- **Pattern recognition** (regular expressions)
- **Categorical classification** (DFA)
- **Scoring transformation** (FST)
- **Structural validation** (CFG)