# Monthly Budget App

A multi-month personal budgeting tool written in Python. Walks you through
income and expense entry for any number of months, then renders a set of
charts to make spending patterns and savings goals visible at a glance.

Built as a personal project to practice the foundations of Python — variables,
control flow, collections, and data visualization — on a problem I actually
care about (tracking my own monthly spending while budgeting for grad school).

## Features

- **Multi-month tracking** — enter as many months as you want in one session
- **Categorized expenses** — split into needs vs wants with custom categories
- **Savings goals** — set a target and see progress against it
- **Visualizations** — pie chart by category, line chart over time, seasonal patterns
- **Personalized tips** — recommendations based on your actual spending mix and stated goal (travel, debt payoff, savings, etc.)
- **50/30/20 rule check** — flags whether your needs/wants/savings split lines up with the recommended budget rule

## Tech Stack

- **Python 3.10+**
- `pandas`, `numpy` — data handling
- `matplotlib`, `seaborn` — charts

## Run It

```bash
pip install -r requirements.txt
jupyter notebook Monthly_Budgeting_App.ipynb
```

Then run the cells top to bottom and answer the prompts.

## Files

| File | What it is |
| --- | --- |
| `Monthly_Budgeting_App.ipynb` | Main notebook — interactive budget app + visuals |
| `Budgeting app final presentation.pptx` | Slide deck walking through the design and screenshots |

## Concepts Practiced

Per the comments in the source: variables, input/output, numeric types, math,
strings (format/split/join/slice), lists/tuples/sets/dicts, if/else, while/for,
range(), break/continue, loop-else, list nesting, nested loops, membership and
identity operators.

## License

[MIT](LICENSE) — feel free to use as a starting point for your own budget app.
