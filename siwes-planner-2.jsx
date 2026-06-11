import { useState } from "react";

const PHASES = [
  { id: 1, name: "Python Consolidation", range: "Weeks 8–10", color: "#2563eb", light: "#dbeafe" },
  { id: 2, name: "Data Science Foundations", range: "Weeks 11–15", color: "#7c3aed", light: "#ede9fe" },
  { id: 3, name: "Data Analysis Project", range: "Weeks 16–18", color: "#0e7490", light: "#cffafe" },
  { id: 4, name: "Machine Learning", range: "Weeks 19–21", color: "#c2410c", light: "#fed7aa" },
  { id: 5, name: "Capstone Project", range: "Weeks 22–23", color: "#b91c1c", light: "#fee2e2" },
  { id: 6, name: "Final Wrap-Up", range: "Week 24", color: "#15803d", light: "#dcfce7" },
];

const WEEKS = [
  { week: 8, phase: 1, theme: "OOP Practice + Python Strengthening", python: "Day 24–28", logbook: "8–12",
    siwesTask: "Deepen your Python OOP skills through daily practice and build a small class-based project.",
    deliverable: "Student Record system using classes → GitHub",
    days: [
      { day: "Monday", tasks: ["Logbook 8", "Python day 24", "LinkedIn post", "SIWES: Review OOP basics — class, object, __init__, self. Write 3 simple example classes in a new .py file."] },
      { day: "Tuesday", tasks: ["Logbook 9", "Python day 25", "SIWES: Build a 'Book' class with title, author, pages. Add 3 methods: summary(), is_long(), get_info()."] },
      { day: "Wednesday", tasks: ["Logbook 10 & 11", "Python day 26", "LinkedIn post", "GitHub push", "SIWES: Learn inheritance — create a 'Textbook' class that extends 'Book'. Add 2 new attributes."] },
      { day: "Thursday", tasks: ["Logbook 12", "Python day 27", "SIWES: Build a Student Record system — name, grade, scores. Add a method to compute the class average."] },
      { day: "Friday", tasks: ["Python day 28", "LinkedIn post", "Medium post — 'Week 8: Going Deeper with Python OOP'", "Weekly review: Rate the week 1–10. Write 1 thing to improve next week."] },
    ]
  },
  { week: 9, phase: 1, theme: "File Handling + Error Management", python: "Day 29–33", logbook: "13–17",
    siwesTask: "Learn to read/write files and handle errors — core skills every Python developer needs.",
    deliverable: "Text-based note saver app → GitHub",
    days: [
      { day: "Monday", tasks: ["Logbook 13", "Python day 29", "LinkedIn post", "SIWES: Learn open(), read(), write(), close(). Practice reading and writing a simple .txt file."] },
      { day: "Tuesday", tasks: ["Logbook 14", "Python day 30", "SIWES: Error handling — try, except, finally. Handle FileNotFoundError and ValueError with examples."] },
      { day: "Wednesday", tasks: ["Logbook 15 & 16", "Python day 31", "LinkedIn post", "GitHub push", "SIWES: Combine files + errors: read a file, handle if missing, write output to a new file."] },
      { day: "Thursday", tasks: ["Logbook 17", "Python day 32", "SIWES: Build a note saver — user types a note, it saves to .txt and can be read back anytime."] },
      { day: "Friday", tasks: ["Python day 33", "LinkedIn post", "Medium post — 'Week 9: Files and Errors in Python'", "Weekly review"] },
    ]
  },
  { week: 10, phase: 1, theme: "APIs + Python Mini Project", python: "Day 34–38", logbook: "18–22",
    siwesTask: "Learn to connect Python to the internet using APIs — a real-world must-have skill.",
    deliverable: "Weather checker or joke app using a free API → GitHub",
    days: [
      { day: "Monday", tasks: ["Logbook 18", "Python day 34", "LinkedIn post", "SIWES: What is an API? What is JSON? Read a beginner guide and write a summary in your own words."] },
      { day: "Tuesday", tasks: ["Logbook 19", "Python day 35", "SIWES: Install requests library. Call a free API (joke or weather API). Print the raw response."] },
      { day: "Wednesday", tasks: ["Logbook 20 & 21", "Python day 36", "LinkedIn post", "GitHub push", "SIWES: Parse the JSON response — extract specific fields and display them cleanly."] },
      { day: "Thursday", tasks: ["Logbook 22", "Python day 37", "SIWES: Build a small interactive app — weather checker or joke generator using input() and the API."] },
      { day: "Friday", tasks: ["Python day 38", "LinkedIn post", "Medium post — 'Week 10: I Made Python Talk to the Internet'", "Weekly review + Phase 1 complete ✓"] },
    ]
  },
  { week: 11, phase: 2, theme: "NumPy Basics", python: "Day 39–43", logbook: "23–27",
    siwesTask: "Set up your data science environment and get comfortable with NumPy arrays.",
    deliverable: "NumPy exercises + student marks stats script → GitHub: Week11-NumPy/",
    days: [
      { day: "Monday", tasks: ["Logbook 23", "Python day 39", "LinkedIn post", "SIWES: Install NumPy. Understand why arrays beat Python lists for numbers. Create your first numpy array."] },
      { day: "Tuesday", tasks: ["Logbook 24", "Python day 40", "SIWES: Practice array indexing, slicing, and reshaping. Write 5 short exercises in a .py file."] },
      { day: "Wednesday", tasks: ["Logbook 25 & 26", "Python day 41", "LinkedIn post", "GitHub push", "SIWES: NumPy math — sum, mean, max, min, std. Apply to an array of 20 numbers. Print all results."] },
      { day: "Thursday", tasks: ["Logbook 27", "Python day 42", "SIWES: Student marks script — store marks in a NumPy array, compute class average, highest and lowest score."] },
      { day: "Friday", tasks: ["Python day 43", "LinkedIn post", "Medium post — 'Week 11: What is NumPy and Why Data Scientists Love It'", "Weekly review"] },
    ]
  },
  { week: 12, phase: 2, theme: "Pandas Introduction", python: "Day 44–48", logbook: "28–32",
    siwesTask: "Learn pandas — the most important Python library for working with real data.",
    deliverable: "First pandas DataFrame exploration → GitHub: Week12-Pandas-Intro/",
    days: [
      { day: "Monday", tasks: ["Logbook 28", "Python day 44", "LinkedIn post", "SIWES: Install pandas. Understand Series vs DataFrame. Create a DataFrame from a Python dictionary."] },
      { day: "Tuesday", tasks: ["Logbook 29", "Python day 45", "SIWES: Read a CSV file with pd.read_csv(). Print first 5 rows with .head(). Find a free CSV on Kaggle."] },
      { day: "Wednesday", tasks: ["Logbook 30 & 31", "Python day 46", "LinkedIn post", "GitHub push", "SIWES: Explore the data — .info(), .describe(), .shape, column names. Write your observations."] },
      { day: "Thursday", tasks: ["Logbook 32", "Python day 47", "SIWES: Select specific columns, filter rows by condition, sort the DataFrame by one column."] },
      { day: "Friday", tasks: ["Python day 48", "LinkedIn post", "Medium post — 'Week 12: My First Time Exploring Real Data with Pandas'", "Weekly review"] },
    ]
  },
  { week: 13, phase: 2, theme: "Pandas — Data Exploration", python: "Day 49–53", logbook: "33–37",
    siwesTask: "Go deeper into pandas — explore, filter, group, and summarize data.",
    deliverable: "Exploration script answering 3 real questions → GitHub: Week13-Pandas-Explore/",
    days: [
      { day: "Monday", tasks: ["Logbook 33", "Python day 49", "LinkedIn post", "SIWES: Select columns and rows with df['col'], df.loc[], df.iloc[]. Practice with your dataset."] },
      { day: "Tuesday", tasks: ["Logbook 34", "Python day 50", "SIWES: Filter rows using conditions (e.g. age > 25, salary == 'High'). Try 3 different conditions."] },
      { day: "Wednesday", tasks: ["Logbook 35 & 36", "Python day 51", "LinkedIn post", "GitHub push", "SIWES: Sort with .sort_values(), count with .value_counts(), find unique values with .unique()."] },
      { day: "Thursday", tasks: ["Logbook 37", "Python day 52", "SIWES: GroupBy — group data by a category, compute mean/sum. Answer 3 real questions from your dataset."] },
      { day: "Friday", tasks: ["Python day 53", "LinkedIn post", "Medium post — 'Week 13: How to Ask Questions from Data Using Pandas'", "Weekly review"] },
    ]
  },
  { week: 14, phase: 2, theme: "Pandas — Data Cleaning", python: "Day 54–58", logbook: "38–42",
    siwesTask: "Learn data cleaning — the most critical and time-consuming real-world data science skill.",
    deliverable: "Fully cleaned dataset saved as CSV → GitHub: Week14-Data-Cleaning/",
    days: [
      { day: "Monday", tasks: ["Logbook 38", "Python day 54", "LinkedIn post", "SIWES: Find missing values with .isnull().sum(). Understand why real datasets always have missing values."] },
      { day: "Tuesday", tasks: ["Logbook 39", "Python day 55", "SIWES: Handle missing values — drop rows with .dropna() or fill with .fillna(). Know when to use which."] },
      { day: "Wednesday", tasks: ["Logbook 40 & 41", "Python day 56", "LinkedIn post", "GitHub push", "SIWES: Rename columns, fix data types with .astype(), remove duplicates with .drop_duplicates()."] },
      { day: "Thursday", tasks: ["Logbook 42", "Python day 57", "SIWES: Take a messy dataset and clean it fully, step by step. Save the cleaned version as a new CSV."] },
      { day: "Friday", tasks: ["Python day 58", "LinkedIn post", "Medium post — 'Week 14: Why Dirty Data is the Biggest Problem in Data Science'", "Weekly review"] },
    ]
  },
  { week: 15, phase: 2, theme: "Matplotlib — Data Visualization", python: "Day 59–63", logbook: "43–47",
    siwesTask: "Turn numbers into charts — learn Matplotlib, the foundation of Python visualization.",
    deliverable: "5 chart types on one dataset → GitHub: Week15-Matplotlib/",
    days: [
      { day: "Monday", tasks: ["Logbook 43", "Python day 59", "LinkedIn post", "SIWES: Why does visualization matter? Install matplotlib. Plot a simple line chart on any data."] },
      { day: "Tuesday", tasks: ["Logbook 44", "Python day 60", "SIWES: Bar chart and histogram. Add title, axis labels, and custom colors to both."] },
      { day: "Wednesday", tasks: ["Logbook 45 & 46", "Python day 61", "LinkedIn post", "GitHub push", "SIWES: Scatter plot — plot two columns against each other. What pattern do you see?"] },
      { day: "Thursday", tasks: ["Logbook 47", "Python day 62", "SIWES: Subplots — create a 2×2 figure with 4 different charts. Save the whole figure as a PNG."] },
      { day: "Friday", tasks: ["Python day 63", "LinkedIn post", "Medium post — 'Week 15: Turning Numbers Into Charts with Matplotlib'", "Weekly review + Phase 2 complete ✓"] },
    ]
  },
  { week: 16, phase: 3, theme: "Seaborn + Advanced Visualization", python: "Day 64–68", logbook: "48–52",
    siwesTask: "Level up with Seaborn and learn to read correlations in data.",
    deliverable: "Seaborn chart set + correlation heatmap → GitHub: Week16-Seaborn/",
    days: [
      { day: "Monday", tasks: ["Logbook 48", "Python day 64", "LinkedIn post", "SIWES: Install Seaborn. Plot a barplot and countplot. Notice how much less code it takes vs matplotlib."] },
      { day: "Tuesday", tasks: ["Logbook 49", "Python day 65", "SIWES: Seaborn heatmap — compute correlation matrix. Understand what positive and negative correlations mean."] },
      { day: "Wednesday", tasks: ["Logbook 50 & 51", "Python day 66", "LinkedIn post", "GitHub push", "SIWES: Boxplot and violin plot — understand data distribution and how to spot outliers."] },
      { day: "Thursday", tasks: ["Logbook 52", "Python day 67", "SIWES: Combine matplotlib and seaborn — build a 4-chart summary of your dataset with clear titles."] },
      { day: "Friday", tasks: ["Python day 68", "LinkedIn post", "Medium post — 'Week 16: Beautiful Visualizations with Seaborn'", "Weekly review"] },
    ]
  },
  { week: 17, phase: 3, theme: "Mini Data Analysis Project", python: "Day 69–73", logbook: "53–57",
    siwesTask: "Apply everything from Phase 2 — do a complete data analysis on a real-world dataset.",
    deliverable: "Full project: load → clean → analyze → visualize → GitHub: Week17-Data-Project/",
    days: [
      { day: "Monday", tasks: ["Logbook 53", "Python day 69", "LinkedIn post", "SIWES: Choose a dataset (Titanic, World Population, or any free Kaggle CSV). Load and explore it."] },
      { day: "Tuesday", tasks: ["Logbook 54", "Python day 70", "SIWES: Clean the dataset — missing values, data types, duplicates. Comment every step."] },
      { day: "Wednesday", tasks: ["Logbook 55 & 56", "Python day 71", "LinkedIn post", "GitHub push", "SIWES: Analyze — answer 5 real questions using groupby, filtering, and aggregation."] },
      { day: "Thursday", tasks: ["Logbook 57", "Python day 72", "SIWES: Visualize — create 4 charts showing your findings. Clear titles and labels on all charts."] },
      { day: "Friday", tasks: ["Python day 73", "LinkedIn post", "Medium post — 'Week 17: My First Complete Data Analysis Project'", "Weekly review"] },
    ]
  },
  { week: 18, phase: 3, theme: "Document + Present Findings", python: "Day 74–78", logbook: "58–62",
    siwesTask: "Polish your Week 17 project so anyone can read, understand, and learn from it.",
    deliverable: "Polished project with README → GitHub updated",
    days: [
      { day: "Monday", tasks: ["Logbook 58", "Python day 74", "LinkedIn post", "SIWES: Write a README for your Week 17 project — dataset, questions, methods, findings."] },
      { day: "Tuesday", tasks: ["Logbook 59", "Python day 75", "SIWES: Polish the code — add comments, clean variable names, make it readable for others."] },
      { day: "Wednesday", tasks: ["Logbook 60 & 61", "Python day 76", "LinkedIn post", "GitHub push — update repo with polished code and README", "SIWES: Check GitHub displays correctly. Fix any missing files or broken links."] },
      { day: "Thursday", tasks: ["Logbook 62", "Python day 77", "SIWES: Logbook reflection on Phase 2 & 3 — what you learned, what was hard, what surprised you."] },
      { day: "Friday", tasks: ["Python day 78", "LinkedIn post", "Medium post — '8 Weeks of Data Science at AI Hub — What I Built'", "Weekly review + Phase 3 complete ✓"] },
    ]
  },
  { week: 19, phase: 4, theme: "Machine Learning — Theory + Setup", python: "Day 79–83", logbook: "63–67",
    siwesTask: "Understand what Machine Learning really is before writing a single line of ML code.",
    deliverable: "ML theory notes + scikit-learn setup → GitHub: Week19-ML-Intro/",
    days: [
      { day: "Monday", tasks: ["Logbook 63", "Python day 79", "LinkedIn post", "SIWES: What is Machine Learning? Supervised vs unsupervised vs reinforcement. Write notes in your own words."] },
      { day: "Tuesday", tasks: ["Logbook 64", "Python day 80", "SIWES: What is a model? What are features and labels? What is training vs testing? Define each in plain English."] },
      { day: "Wednesday", tasks: ["Logbook 65 & 66", "Python day 81", "LinkedIn post", "GitHub push", "SIWES: Install scikit-learn. Load the built-in Iris dataset. Print its features, target names, and shape."] },
      { day: "Thursday", tasks: ["Logbook 67", "Python day 82", "SIWES: Train/test split — what it is and why 80/20. Write the code and observe the sizes of your splits."] },
      { day: "Friday", tasks: ["Python day 83", "LinkedIn post", "Medium post — 'Week 19: What is Machine Learning? A Beginner's Honest Explanation'", "Weekly review"] },
    ]
  },
  { week: 20, phase: 4, theme: "Linear Regression", python: "Day 84–88", logbook: "68–72",
    siwesTask: "Build and evaluate your first real ML model — a Linear Regression predictor.",
    deliverable: "Trained regression model + evaluation → GitHub: Week20-Regression/",
    days: [
      { day: "Monday", tasks: ["Logbook 68", "Python day 84", "LinkedIn post", "SIWES: What is regression? Real examples — house prices, salary prediction. Write 3 examples yourself."] },
      { day: "Tuesday", tasks: ["Logbook 69", "Python day 85", "SIWES: Load a dataset. Identify features (X) and target (y). Do a train/test split. Print the shapes."] },
      { day: "Wednesday", tasks: ["Logbook 70 & 71", "Python day 86", "LinkedIn post", "GitHub push", "SIWES: Train a LinearRegression model — .fit(), .predict(). Print 5 predicted vs actual values side by side."] },
      { day: "Thursday", tasks: ["Logbook 72", "Python day 87", "SIWES: Evaluate with MAE and R² score. Write in plain English what each number says about your model's quality."] },
      { day: "Friday", tasks: ["Python day 88", "LinkedIn post", "Medium post — 'Week 20: I Trained My First ML Model — Here's What Happened'", "Weekly review"] },
    ]
  },
  { week: 21, phase: 4, theme: "Classification Models", python: "Day 89–93", logbook: "73–77",
    siwesTask: "Learn classification — train a model to put data into categories.",
    deliverable: "KNN + Decision Tree comparison → GitHub: Week21-Classification/",
    days: [
      { day: "Monday", tasks: ["Logbook 73", "Python day 89", "LinkedIn post", "SIWES: What is classification? Examples: spam detection, disease diagnosis. How is it different from regression?"] },
      { day: "Tuesday", tasks: ["Logbook 74", "Python day 90", "SIWES: Train a K-Nearest Neighbors (KNN) classifier on the Iris dataset. Print the accuracy score."] },
      { day: "Wednesday", tasks: ["Logbook 75 & 76", "Python day 91", "LinkedIn post", "GitHub push", "SIWES: Evaluate KNN — confusion matrix and classification report. Visualize the matrix with Seaborn."] },
      { day: "Thursday", tasks: ["Logbook 77", "Python day 92", "SIWES: Train a Decision Tree on same dataset. Compare accuracy with KNN. Write when to use each."] },
      { day: "Friday", tasks: ["Python day 93", "LinkedIn post", "Medium post — 'Week 21: Teaching a Computer to Classify — KNN vs Decision Trees'", "Weekly review + Phase 4 complete ✓"] },
    ]
  },
  { week: 22, phase: 5, theme: "Capstone — Plan + Build", python: "Day 94–98", logbook: "78–82",
    siwesTask: "Begin your SIWES capstone — an end-to-end ML project from scratch on a dataset of your choice.",
    deliverable: "Capstone project (in progress) → GitHub: Week22-Capstone/",
    days: [
      { day: "Monday", tasks: ["Logbook 78", "Python day 94", "LinkedIn post", "SIWES: Choose your capstone dataset. Define the problem clearly — what question are you answering with ML?"] },
      { day: "Tuesday", tasks: ["Logbook 79", "Python day 95", "SIWES: Load, explore, and clean the capstone dataset. Comment every step as you go."] },
      { day: "Wednesday", tasks: ["Logbook 80 & 81", "Python day 96", "LinkedIn post", "GitHub push", "SIWES: Analyze and visualize — create 3 charts that show meaningful findings from the data."] },
      { day: "Thursday", tasks: ["Logbook 82", "Python day 97", "SIWES: Train an ML model on the capstone data. Evaluate it. Write in plain English what the results mean."] },
      { day: "Friday", tasks: ["Python day 98", "LinkedIn post", "Medium post — 'Week 22: My SIWES Capstone Has Begun — Here's the Plan'", "Weekly review"] },
    ]
  },
  { week: 23, phase: 5, theme: "Capstone — Polish + Publish", python: "Day 99–100 🎉", logbook: "83–87",
    siwesTask: "Polish your capstone code, write the README, and publish the final project publicly.",
    deliverable: "Complete polished capstone with README → GitHub: Week23-Capstone-Final/",
    days: [
      { day: "Monday", tasks: ["Logbook 83", "Python day 99", "LinkedIn post", "SIWES: Polish capstone code — comments, clean variable names, organize into functions where possible."] },
      { day: "Tuesday", tasks: ["Logbook 84", "🎉 Python day 100 — 100 Days of Python COMPLETE!", "SIWES: Write the capstone README — overview, dataset, methods, results, conclusions."] },
      { day: "Wednesday", tasks: ["Logbook 85 & 86", "🎉 LinkedIn post — celebrate finishing 100 Days of Python!", "GitHub final push — complete capstone submission", "SIWES: Review all GitHub folders. Every week should have at least a basic README."] },
      { day: "Thursday", tasks: ["Logbook 87", "SIWES: Write your SIWES logbook summary — all phases covered, skills gained, biggest lessons learned, personal growth."] },
      { day: "Friday", tasks: ["LinkedIn post — share your capstone project publicly with a link", "Medium post — 'My SIWES Capstone: An End-to-End ML Project Explained Simply'", "🎉 Rest. You earned it."] },
    ]
  },
  { week: 24, phase: 6, theme: "Final Wrap-Up", python: "Course Complete ✓", logbook: "88–92",
    siwesTask: "Close out your SIWES placement — clean your repo, write your report, update your profile.",
    deliverable: "Clean GitHub repo + Final SIWES report + Updated LinkedIn profile",
    days: [
      { day: "Monday", tasks: ["Logbook 88", "LinkedIn post", "SIWES: Organize SIWES-AI-JOURNEY repo — clean folder names, add READMEs to any folder missing one."] },
      { day: "Tuesday", tasks: ["Logbook 89", "SIWES: Write the final SIWES report — cover all 6 phases, key projects, skills gained, and lessons learned."] },
      { day: "Wednesday", tasks: ["Logbook 90 & 91", "LinkedIn post", "GitHub final push — complete repo cleanup", "SIWES: Update LinkedIn with SIWES experience, skills (Python, pandas, NumPy, scikit-learn, Matplotlib), and GitHub links."] },
      { day: "Thursday", tasks: ["Logbook 92", "SIWES: Final logbook entry — reflect on who you were at Week 1 vs who you are now. Be honest. Write it properly."] },
      { day: "Friday", tasks: ["LinkedIn post — share your full SIWES journey publicly", "Medium post — '6 Months of Self-Directed AI/ML SIWES — What I Really Learned'", "🎓 SIWES COMPLETE. You did it, Sadiq."] },
    ]
  },
];

function getTag(task) {
  if (task.startsWith("Logbook")) return { label: "LOGBOOK", color: "#7c3aed" };
  if (task.toLowerCase().includes("python day") || task.includes("Days of Python")) return { label: "PYTHON", color: "#2563eb" };
  if (task.startsWith("LinkedIn")) return { label: "LINKEDIN", color: "#0369a1" };
  if (task.startsWith("Medium")) return { label: "MEDIUM", color: "#047857" };
  if (task.startsWith("GitHub")) return { label: "GITHUB", color: "#374151" };
  if (task.startsWith("SIWES")) return { label: "SIWES", color: "#c2410c" };
  if (task.startsWith("Weekly review")) return { label: "REVIEW", color: "#92400e" };
  if (task.includes("🎉") || task.includes("🎓") || task.includes("✓")) return { label: "MILESTONE", color: "#065f46" };
  return { label: null, color: "#374151" };
}

export default function SIWESPlanner() {
  const [activePhase, setActivePhase] = useState(1);
  const [activeWeek, setActiveWeek] = useState(8);
  const [activeDay, setActiveDay] = useState(0);
  const [checked, setChecked] = useState({});

  const toggle = (w, d, t) => {
    const k = `${w}-${d}-${t}`;
    setChecked(p => ({ ...p, [k]: !p[k] }));
  };
  const isDone = (w, d, t) => !!checked[`${w}-${d}-${t}`];

  const weekProg = (wNum) => {
    const wk = WEEKS.find(x => x.week === wNum);
    if (!wk) return 0;
    let done = 0, total = 0;
    wk.days.forEach((day, d) => day.tasks.forEach((_, t) => { total++; if (isDone(wNum, d, t)) done++; }));
    return total > 0 ? Math.round((done / total) * 100) : 0;
  };

  const phaseProg = (pid) => {
    let done = 0, total = 0;
    WEEKS.filter(w => w.phase === pid).forEach(w => w.days.forEach((day, d) =>
      day.tasks.forEach((_, t) => { total++; if (isDone(w.week, d, t)) done++; })
    ));
    return total > 0 ? Math.round((done / total) * 100) : 0;
  };

  const overall = () => {
    let done = 0, total = 0;
    WEEKS.forEach(w => w.days.forEach((day, d) =>
      day.tasks.forEach((_, t) => { total++; if (isDone(w.week, d, t)) done++; })
    ));
    return total > 0 ? Math.round((done / total) * 100) : 0;
  };

  const dayProg = (wNum, d) => {
    const wk = WEEKS.find(x => x.week === wNum);
    if (!wk) return { done: 0, total: 0 };
    const tasks = wk.days[d].tasks;
    return { done: tasks.filter((_, t) => isDone(wNum, d, t)).length, total: tasks.length };
  };

  const phaseWeeks = WEEKS.filter(w => w.phase === activePhase);
  const phase = PHASES.find(p => p.id === activePhase);
  const week = WEEKS.find(w => w.week === activeWeek) || phaseWeeks[0];
  const day = week?.days[activeDay];
  const wp = weekProg(activeWeek);
  const dp = dayProg(activeWeek, activeDay);
  const ov = overall();

  const card = { backgroundColor: "white", borderRadius: "12px", border: "1px solid #e2e8f0", boxShadow: "0 1px 4px rgba(0,0,0,0.06)" };

  return (
    <div style={{ backgroundColor: "#f1f5f9", minHeight: "100vh", fontFamily: "'Segoe UI', system-ui, sans-serif", padding: "16px", color: "#0f172a" }}>

      {/* Header */}
      <div style={{ ...card, padding: "16px", marginBottom: "14px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "6px" }}>
          <div style={{ width: "8px", height: "8px", borderRadius: "50%", backgroundColor: phase?.color }} />
          <span style={{ color: phase?.color, fontSize: "10px", fontWeight: "700", letterSpacing: "2px" }}>AI HUB · SIWES PLACEMENT</span>
        </div>
        <h1 style={{ fontSize: "20px", fontWeight: "800", margin: "0 0 2px 0" }}>SIWES Planner</h1>
        <p style={{ color: "#64748b", fontSize: "11px", margin: "0 0 12px 0" }}>Weeks 8–24 · Sadiq Nagoda · AI/ML Track</p>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
          <span style={{ fontSize: "11px", color: "#64748b", fontWeight: "600" }}>Overall Progress</span>
          <span style={{ fontSize: "11px", fontWeight: "800", color: ov > 0 ? "#16a34a" : "#cbd5e1" }}>{ov}%</span>
        </div>
        <div style={{ height: "5px", backgroundColor: "#e2e8f0", borderRadius: "3px", overflow: "hidden" }}>
          <div style={{ height: "100%", width: `${ov}%`, backgroundColor: "#16a34a", borderRadius: "3px", transition: "width 0.4s" }} />
        </div>
      </div>

      {/* Phases */}
      <div style={{ marginBottom: "14px" }}>
        <p style={{ fontSize: "10px", fontWeight: "700", color: "#94a3b8", letterSpacing: "2px", textTransform: "uppercase", margin: "0 0 8px 0" }}>Phases</p>
        <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
          {PHASES.map(p => {
            const pp = phaseProg(p.id);
            const isA = activePhase === p.id;
            return (
              <button key={p.id} onClick={() => {
                setActivePhase(p.id);
                const first = WEEKS.find(w => w.phase === p.id);
                if (first) { setActiveWeek(first.week); setActiveDay(0); }
              }} style={{
                display: "flex", alignItems: "center", gap: "10px", padding: "10px 14px",
                borderRadius: "10px", border: `1.5px solid ${isA ? p.color : "#e2e8f0"}`,
                backgroundColor: isA ? p.light : "white", cursor: "pointer", textAlign: "left",
                boxShadow: isA ? `0 0 0 3px ${p.color}18` : "none", transition: "all 0.15s"
              }}>
                <div style={{ width: "10px", height: "10px", borderRadius: "50%", backgroundColor: p.color, flexShrink: 0 }} />
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: "13px", fontWeight: "700", color: isA ? p.color : "#1e293b" }}>{p.name}</div>
                  <div style={{ fontSize: "10px", color: "#94a3b8" }}>{p.range}</div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontSize: "13px", fontWeight: "800", color: pp > 0 ? "#16a34a" : "#cbd5e1" }}>{pp}%</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Week tabs */}
      <div style={{ marginBottom: "14px" }}>
        <p style={{ fontSize: "10px", fontWeight: "700", color: "#94a3b8", letterSpacing: "2px", textTransform: "uppercase", margin: "0 0 8px 0" }}>Weeks</p>
        <div style={{ display: "flex", gap: "6px", overflowX: "auto", paddingBottom: "4px" }}>
          {phaseWeeks.map(w => {
            const wp2 = weekProg(w.week);
            const isA = activeWeek === w.week;
            return (
              <button key={w.week} onClick={() => { setActiveWeek(w.week); setActiveDay(0); }} style={{
                flexShrink: 0, minWidth: "60px", padding: "8px 12px", borderRadius: "8px",
                border: `1.5px solid ${isA ? phase?.color : "#e2e8f0"}`,
                backgroundColor: isA ? phase?.color : "white",
                color: isA ? "white" : "#374151", cursor: "pointer",
                fontSize: "11px", fontWeight: "700", textAlign: "center", transition: "all 0.15s"
              }}>
                <div>W{w.week}</div>
                <div style={{ fontSize: "10px", opacity: 0.85, marginTop: "2px" }}>{wp2}%</div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Week card */}
      {week && (
        <div style={{ ...card, padding: "16px", marginBottom: "14px", borderLeft: `4px solid ${phase?.color}` }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "10px", flexWrap: "wrap" }}>
            <span style={{ backgroundColor: phase?.light, color: phase?.color, fontSize: "10px", fontWeight: "800", padding: "3px 10px", borderRadius: "20px" }}>WEEK {week.week}</span>
            <span style={{ fontSize: "13px", fontWeight: "700" }}>{week.theme}</span>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px", marginBottom: "12px" }}>
            <div style={{ backgroundColor: "#f8fafc", borderRadius: "8px", padding: "8px 10px" }}>
              <div style={{ fontSize: "9px", color: "#94a3b8", fontWeight: "700", letterSpacing: "1px", marginBottom: "2px" }}>PYTHON</div>
              <div style={{ fontSize: "12px", fontWeight: "700", color: "#2563eb" }}>{week.python}</div>
            </div>
            <div style={{ backgroundColor: "#f8fafc", borderRadius: "8px", padding: "8px 10px" }}>
              <div style={{ fontSize: "9px", color: "#94a3b8", fontWeight: "700", letterSpacing: "1px", marginBottom: "2px" }}>LOGBOOK</div>
              <div style={{ fontSize: "12px", fontWeight: "700", color: "#7c3aed" }}>Entries {week.logbook}</div>
            </div>
          </div>
          <div style={{ backgroundColor: "#f8fafc", borderRadius: "8px", padding: "10px 12px", borderLeft: `3px solid ${phase?.color}`, marginBottom: "8px" }}>
            <div style={{ fontSize: "9px", color: "#94a3b8", fontWeight: "700", letterSpacing: "1px", marginBottom: "3px" }}>SIWES TASK</div>
            <div style={{ fontSize: "12px", color: "#334155", lineHeight: "1.6" }}>{week.siwesTask}</div>
          </div>
          <div style={{ backgroundColor: "#f0fdf4", borderRadius: "8px", padding: "10px 12px", borderLeft: "3px solid #16a34a", marginBottom: "12px" }}>
            <div style={{ fontSize: "9px", color: "#94a3b8", fontWeight: "700", letterSpacing: "1px", marginBottom: "3px" }}>DELIVERABLE</div>
            <div style={{ fontSize: "12px", color: "#166534", lineHeight: "1.6" }}>{week.deliverable}</div>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "5px" }}>
            <span style={{ fontSize: "11px", color: "#64748b" }}>Week Progress</span>
            <span style={{ fontSize: "11px", fontWeight: "700", color: wp === 100 ? "#16a34a" : phase?.color }}>{wp}%</span>
          </div>
          <div style={{ height: "4px", backgroundColor: "#e2e8f0", borderRadius: "2px", overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${wp}%`, backgroundColor: wp === 100 ? "#16a34a" : phase?.color, borderRadius: "2px", transition: "width 0.3s" }} />
          </div>
        </div>
      )}

      {/* Day tabs */}
      <div style={{ display: "flex", gap: "6px", marginBottom: "12px", overflowX: "auto", paddingBottom: "2px" }}>
        {week?.days.map((d, i) => {
          const p = dayProg(activeWeek, i);
          const done = p.done === p.total && p.total > 0;
          const isA = activeDay === i;
          return (
            <button key={i} onClick={() => setActiveDay(i)} style={{
              flexShrink: 0, minWidth: "58px", padding: "8px 10px", borderRadius: "8px",
              border: `1.5px solid ${isA ? phase?.color : done ? "#16a34a" : "#e2e8f0"}`,
              backgroundColor: isA ? phase?.color : done ? "#f0fdf4" : "white",
              color: isA ? "white" : done ? "#16a34a" : "#374151",
              cursor: "pointer", fontSize: "11px", fontWeight: "700", textAlign: "center", transition: "all 0.15s"
            }}>
              <div>{d.day.substring(0, 3).toUpperCase()}</div>
              <div style={{ fontSize: "10px", opacity: 0.85, marginTop: "2px" }}>{p.done}/{p.total}</div>
            </button>
          );
        })}
      </div>

      {/* Tasks */}
      {day && (
        <div style={{ ...card, padding: "16px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px" }}>
            <div>
              <h3 style={{ margin: "0 0 2px 0", fontSize: "17px", fontWeight: "800" }}>{day.day}</h3>
              <p style={{ margin: 0, fontSize: "11px", color: "#94a3b8" }}>Week {activeWeek} · {dp.done}/{dp.total} tasks</p>
            </div>
            {dp.done === dp.total && dp.total > 0 && (
              <span style={{ backgroundColor: "#d1fae5", color: "#065f46", fontSize: "10px", fontWeight: "800", padding: "4px 12px", borderRadius: "20px" }}>✓ DONE</span>
            )}
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            {day.tasks.map((task, t) => {
              const done = isDone(activeWeek, activeDay, t);
              const tag = getTag(task);
              return (
                <div key={t} onClick={() => toggle(activeWeek, activeDay, t)} style={{
                  display: "flex", alignItems: "flex-start", gap: "10px", padding: "11px 13px",
                  borderRadius: "8px", cursor: "pointer",
                  backgroundColor: done ? "#f8fafc" : "white",
                  border: `1px solid ${done ? "#e2e8f0" : tag.color + "25"}`,
                  transition: "all 0.15s", opacity: done ? 0.6 : 1
                }}>
                  <div style={{
                    marginTop: "2px", flexShrink: 0, width: "18px", height: "18px", borderRadius: "5px",
                    border: `2px solid ${done ? "#16a34a" : tag.color}`,
                    backgroundColor: done ? "#16a34a" : "white",
                    display: "flex", alignItems: "center", justifyContent: "center", transition: "all 0.15s"
                  }}>
                    {done && <span style={{ color: "white", fontSize: "11px", fontWeight: "bold" }}>✓</span>}
                  </div>
                  <div style={{ flex: 1 }}>
                    {tag.label && (
                      <span style={{ display: "inline-block", backgroundColor: tag.color, color: "white", fontSize: "9px", fontWeight: "700", padding: "2px 7px", borderRadius: "4px", marginBottom: "4px", letterSpacing: "0.5px" }}>
                        {tag.label}
                      </span>
                    )}
                    <p style={{ margin: 0, fontSize: "12px", lineHeight: "1.55", color: done ? "#94a3b8" : "#1e293b", textDecoration: done ? "line-through" : "none" }}>{task}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <p style={{ textAlign: "center", color: "#cbd5e1", fontSize: "11px", marginTop: "24px" }}>
        AI Hub SIWES · Weeks 8–24 · Built by Sadiq Nagoda
      </p>
    </div>
  );
}
