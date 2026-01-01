from flask import Flask, render_template, request, url_for
import pandas as pd
import os

app = Flask(__name__)

# ================= LOAD DATA =================
df = pd.read_csv("players_20.csv")
df = df.dropna(subset=["short_name"])

# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= PLAYERS =================
@app.route("/players")
def players():
    query = request.args.get("name", "").strip()
    page = request.args.get("page", 1, type=int)

    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    filtered = df
    if query:
        filtered = df[df["short_name"].str.contains(query, case=False, na=False)]

    total_pages = max(1, (len(filtered) // per_page) + 1)

    page_data = filtered.iloc[start:end]

    players_to_show = page_data[[
        "sofifa_id",
        "short_name",
        "nationality",
        "club",
        "player_positions",
        "overall"
    ]].to_dict(orient="records")

    return render_template(
        "players.html",
        players=players_to_show,
        page=page,
        total_pages=total_pages,
        query=query
    )

# ================= PLAYER PROFILE =================
@app.route("/player/<int:sofifa_id>")
def profile(sofifa_id):
    player = df[df["sofifa_id"] == sofifa_id].iloc[0]

    image_path = f"images/{sofifa_id}.png"
    if not os.path.exists(f"static/{image_path}"):
        image_path = "images/default_player.png"

    return render_template(
        "profile.html",
        player=player,
        player_image=image_path
    )

# ================= PROBLEM STATEMENT =================
@app.route("/problem-statement")
def problem_statement():
    return render_template("problem_statement.html")


# ================= COMPARE =================
@app.route("/compare", methods=["GET", "POST"])
def compare():
    result = None

    if request.method == "POST":
        name1 = request.form.get("player1", "").strip().lower()
        name2 = request.form.get("player2", "").strip().lower()

        name_col = "short_name" if "short_name" in df.columns else "long_name"

        p1_df = df[df[name_col].str.lower().str.contains(name1, na=False)]
        p2_df = df[df[name_col].str.lower().str.contains(name2, na=False)]

        if not p1_df.empty and not p2_df.empty:
            p1 = p1_df.iloc[0]
            p2 = p2_df.iloc[0]

            # ===== IMAGE PATHS (NO url_for HERE) =====
            img1 = f"images/{int(p1.sofifa_id)}.png"
            img2 = f"images/{int(p2.sofifa_id)}.png"

            if not os.path.exists(f"static/{img1}"):
                img1 = "images/default_player.png"

            if not os.path.exists(f"static/{img2}"):
                img2 = "images/default_player.png"

            score_cols = ["pace", "shooting", "passing", "dribbling", "physic"]

            p1_score = sum(p1[c] for c in score_cols if pd.notna(p1[c]))
            p2_score = sum(p2[c] for c in score_cols if pd.notna(p2[c]))

            if p1_score > p2_score:
                winner = p1.short_name
                reason = "Higher combined attacking & physical attributes"
            elif p2_score > p1_score:
                winner = p2.short_name
                reason = "Stronger overall skill balance"
            else:
                winner = "Tie"
                reason = "Both players have very similar attributes"

            result = {
                "p1": p1.to_dict(),
                "p2": p2.to_dict(),
                "p1_img": img1,   # ✅ path only
                "p2_img": img2,
                "winner": winner,
                "reason": reason
            }

    return render_template("compare.html", result=result)


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

