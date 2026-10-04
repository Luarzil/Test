import asyncio, subprocess, textwrap, math, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"
OUT.mkdir(exist_ok=True)
W,H=1280,720
VOICE="en-US-JennyNeural"

slides=[
("Trading Research Update","Pulse + Anchor: What We Built So Far",[
"Pulse is now split into Day and Swing.",
"They share one market-intelligence brain and one risk governor.",
"Anchor stays separate for long-term dividend and compounding research.",
"Everything is still research: freeze, test, break, then paper trade."
],"""Here is where the trading project stands after tonight's work. What started as a general trading idea is now becoming a structured research system. Pulse is the active trading engine, split into two specialized parts: Pulse Day for same-session trades, and Pulse Swing for positions intentionally held for several days. Both share one market-intelligence layer and one account-level risk governor. Anchor stays separate as the long-term dividend and compounding engine. Nothing here is considered finished or proven yet. The goal is to build rules that survive unseen historical testing and then paper trading before real money is ever considered."""),

("Pulse Architecture","One Brain, Two Execution Engines",[
"Shared brain: regime, sector, volatility, liquidity, friction, correlation.",
"Horizon is chosen before entry.",
"Day handles hours. Swing handles days.",
"A failed Day trade never becomes a Swing trade just to avoid a loss."
],"""The biggest architectural improvement was separating intelligence from execution. Pulse now has a shared brain that looks at broad market regime, sector strength, volatility, liquidity, transaction friction, correlation, and whether doing nothing is the best decision. A horizon router then decides whether an opportunity belongs to Day or Swing before the trade begins. Pulse Day handles hours. Pulse Swing handles days. Their entries, stops, targets, and holding periods remain separate. That protects us from a dangerous habit: a failed day trade can never quietly become a swing trade just because we do not want to take the loss."""),

("Pulse Day","What We Preserve Immediately",[
"Use real intraday data: one- to five-minute bars, VWAP, opening range and relative volume.",
"First setup family: intraday Continuation.",
"Expected movement must beat friction.",
"Correlated positions share risk, and no trade is a valid decision."
],"""Pulse Day is being preserved as a genuine intraday engine. We will not call next-day daily price action a day-trading backtest. True Day validation needs intraday bars, VWAP, opening-range behavior, relative volume, time of day, and evidence of acceleration or exhaustion. The first Day family we want to validate is Continuation. After a real momentum move begins, can Pulse enter while meaningful movement is still available without buying the exhaustion point? Three principles from Day are strong enough to transfer to Swing: expected movement must be large enough to beat friction, correlated positions should share a risk budget, and no trade is a completely valid output when conditions are weak."""),

("Pulse Swing","Pullback v0.2 — Current Candidate",[
"Signal-day stock gain at least 2%.",
"Relevant sector gain above 1%.",
"Close in the lower 40% of the daily range.",
"Next-session thesis check.",
"Candidate stop: 1.5 times ATR.",
"Risk-sized position, 2R target, maximum five sessions."
],"""Pulse Swing now has a more explicit Pullback research candidate. The signal begins with a stock gaining at least two percent while its relevant sector is also strong. Instead of chasing a stock that closes at the very top of its range, the current hypothesis looks for a deeper pullback, roughly a close in the lower forty percent of the day's range. The next session must still preserve the original thesis. The current stop candidate is one and a half times A T R, which gives each stock room based on its own normal volatility. Position size then adjusts so the dollar risk stays controlled. The current research target is two R, with a maximum hold of five trading sessions."""),

("Risk Governor","Risk Is Not the Same as Money Invested",[
"Research account example: $10,000.",
"Candidate Normal Pulse risk: 1.5%, or $150 planned open risk.",
"2% is a provisional ceiling, not the normal target.",
"Day and Swing compete for the same risk pool.",
"Overnight Swing positions need extra gap-risk treatment."
],"""One of the most important clarifications tonight was the difference between capital deployed and risk consumed. Buying twenty-five hundred dollars of stock does not mean twenty-five hundred dollars is at risk. If the stop implies a fifty-dollar planned loss, then fifty dollars is the risk being consumed. For a ten-thousand-dollar research account, the current candidate Normal Pulse budget is one and a half percent, or one hundred fifty dollars of total planned open risk. Two percent is being treated as a provisional ceiling, not the normal target. Day and Swing compete for the same pool, while Swing receives extra attention because overnight gaps can jump through a stop."""),

("What Testing Already Changed","Bad Rules We Prevented",[
"The old $30 round-trip equity fee was rejected.",
"Use 5, 10 and 20 basis-point friction stress instead.",
"Blindly widening stops did not fix weak trades.",
"A hard 10% signal-day cap was rejected after it would have filtered a later winner.",
"1.5 × ATR is promising, but still only a candidate."
],"""The testing has already prevented several bad rules from becoming permanent. The old thirty-dollar round-trip stock fee was unrealistic, so we replaced it with friction sensitivity at five, ten, and twenty basis points. Simply widening stops did not fix weak trades. A hard ten-percent maximum signal-day move was also rejected because it would have filtered out a later profitable Micron setup. The more promising stop idea was volatility-aware sizing. A one-and-a-half A T R stop performed better than the signal-day-low stop in a small fresh sample, while still allowing AMD to remain a genuine loser. That is exactly what we want from research: rules should not magically erase losses. They should make the process more rational."""),

("Anchor","Long-Term Compounding Stays Separate",[
"Rule 0: dividend and fundamental safety gate before scoring.",
"10-point filter: sustainability, dividend growth, business growth, quality, valuation.",
"Rule 6: favor total-dollar compounding over highest yield.",
"Working portfolio: five holdings, about 20% starting weight.",
"Current caps: 25% per company and 40% per sector."
],"""Anchor remains a different engine with a different job. It looks for sustainable dividends, dividend growth, business growth, quality, valuation, and long-term price appreciation. Rule Zero blocks companies with dividend or fundamental safety problems before scoring. The ten-point quality filter and Rule Six favor total-dollar compounding rather than simply the highest yield. Today's working portfolio structure is five qualified holdings, about twenty percent starting weight each, with a twenty-five-percent maximum in one company and a forty-percent maximum in one sector. Rule Seven allows staged additions during genuine market dislocations, but only while the business thesis remains healthy."""),

("How Day and Swing Learn","Transfer Concepts — Not Blind Rules",[
"Shared: regime, sector, volatility, liquidity, friction, correlation and account risk.",
"Not shared automatically: entry trigger, stop, target, holding period and overnight rules.",
"If Day learns a concept, Swing tests its own multi-day version.",
"If Swing learns a concept, Day tests its own intraday version."
],"""The shared-brain idea gives us a disciplined way for Day and Swing to learn from one another. If Day discovers that transaction friction destroys small expected moves, Swing inherits the concept but applies it to a multi-day horizon. If Swing finds that volatility-aware stops are better than arbitrary stops, Day can test an intraday version without copying the same one-and-a-half A T R number. Market regime, sector confirmation, liquidity, correlation, and account risk can be shared. Exact entries, stops, targets, and holding periods must be independently earned. That gives us one operating system, but two specialized execution engines."""),

("Next Research Phase","Try to Break It Before We Trust It",[
"Freeze Swing Pullback v0.2.",
"Test substantially more unseen history.",
"Include different sectors and hostile market regimes.",
"Compare cluster caps, drawdown, recovery and missed winners.",
"Validate Pulse Day separately with true intraday data.",
"Paper trade before any real-money use."
],"""The next phase is deliberately harder. Pulse Swing Pullback stays frozen while we test more unseen history, different sectors, bull markets, falling markets, and choppy conditions. We will compare friction stress, correlated-cluster limits, regime routing, maximum drawdown, recovery time, losing streaks, and how many good trades the safety rules accidentally reject. Pulse Day will be validated separately with true intraday data. Anchor will continue its own long-horizon stress testing. The operating principle is simple: freeze the rule, test it chronologically, preserve the losses, and only change the rule after the completed test gives us evidence for a new version."""),

("Current Status","Promising — Still Research",[
"Pulse Day: preserved for true intraday testing.",
"Pulse Swing: Pullback v0.2 is the current candidate.",
"Shared Pulse brain: market intelligence plus risk governance.",
"Anchor: long-term quality, dividend and compounding.",
"Next milestone: stronger validation, then paper trading."
],"""So the project is in a promising place, but it is still a research framework rather than a finished trading system. The important progress is not one winning backtest. It is that the architecture is becoming more disciplined: separate horizons, shared intelligence, risk measured correctly, failed hypotheses preserved, and rules frozen before unseen tests. That gives us a much better foundation for the next round. The next milestone is not real-money trading. It is stronger historical validation followed by paper trading. That is where we left the project tonight.""")
]

def find_font(bold=False):
    choices=[
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
      "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for p in choices:
        if Path(p).exists(): return p
    raise RuntimeError("font not found")

def font(size,bold=False):
    return ImageFont.truetype(find_font(bold),size)

def wrap(draw,text,fnt,width):
    words=text.split()
    lines=[]; line=""
    for word in words:
        t=(line+" "+word).strip()
        if draw.textbbox((0,0),t,font=fnt)[2] <= width:
            line=t
        else:
            if line: lines.append(line)
            line=word
    if line: lines.append(line)
    return lines

def render_slide(i,kicker,title,bullets):
    img=Image.new("RGB",(W,H),(13,23,38))
    d=ImageDraw.Draw(img)
    d.rectangle((0,0,W,11),fill=(76,201,192))
    d.text((70,48),kicker.upper(),font=font(23,True),fill=(76,201,192))
    d.text((70,88),title,font=font(45,True),fill=(246,249,252))
    d.rectangle((70,151,1210,154),fill=(76,201,192))
    y=195
    for b in bullets:
        lines=wrap(d,b,font(25,True),980)
        h=58+max(0,len(lines)-1)*31
        d.rounded_rectangle((85,y,1195,y+h),18,fill=(25,37,57),outline=(60,78,101),width=2)
        d.ellipse((112,y+20,132,y+40),fill=(76,201,192))
        ty=y+15
        for line in lines:
            d.text((155,ty),line,font=font(25,True),fill=(229,236,243))
            ty+=31
        y+=h+15
    d.text((70,675),"Research / historical validation / paper-trading preparation only",font=font(17),fill=(151,165,181))
    d.text((1155,675),f"{i}/{len(slides)}",font=font(17,True),fill=(151,165,181))
    return img

async def synth(text,path):
    comm=edge_tts.Communicate(text,VOICE,rate="-3%")
    await comm.save(str(path))

def duration(path):
    p=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(path)],capture_output=True,text=True,check=True)
    return float(p.stdout.strip())

async def main():
    segments=[]
    for i,(k,t,bullets,narr) in enumerate(slides,1):
        png=OUT/f"slide_{i:02d}.png"
        mp3=OUT/f"audio_{i:02d}.mp3"
        seg=OUT/f"seg_{i:02d}.mp4"
        render_slide(i,k,t,bullets).save(png)
        await synth(narr,mp3)
        dur=duration(mp3)+0.55
        subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-framerate","30","-i",str(png),"-i",str(mp3),
                        "-vf","scale=1280:720,format=yuv420p","-af","loudnorm=I=-16:TP=-1.5:LRA=8,apad",
                        "-c:v","libx264","-preset","veryfast","-tune","stillimage","-c:a","aac","-b:a","160k",
                        "-t",f"{dur:.3f}","-shortest",str(seg)],check=True)
        segments.append(seg)
    concat=OUT/"concat.txt"
    concat.write_text("\n".join([f"file '{x.name}'" for x in segments]))
    final=OUT/"Trading_Project_Progress_Pulse_Anchor_JennyNeural.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(concat),"-c","copy","-movflags","+faststart",str(final)],check=True)
    (OUT/"VOICE_AND_BUILD.txt").write_text("Voice: en-US-JennyNeural\nRate: -3%\nThis is the same Microsoft Edge neural voice configured in GateFlow's create-video-refresh.py.\n")
    print(final)

asyncio.run(main())
