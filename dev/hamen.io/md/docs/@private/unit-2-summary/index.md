<doc style="display: none;">
    title: Unit 2 Summary
    titleID: ...
    description: ...
    type: Blog
    tags: ...
    author: Daniel Hamen
    authorID: danielhamen
    date: 2023-08-25
    url: blogs/@private/unit-2-summary
    category: ...
    categorySlug: ...
</doc>

# 2.0: Unit 2 Summary: *Functions: Understanding Rates of Change*

## Introduction

In this summary, we'll discuss the content of Unit 2 in the MHF-4U1, *Grade 12 University-Level Functions*. This summary is split into five parts:

- [2.1&colon; Determining Average Rate of Change]("#-colon-determining-average-rate-of-change")
- [2.2&colon; Estimating Instantaneous Rates of Change: Intervals]("")
- [2.3&colon; Estimating Instantaneous Rates of Change: Algebraic Method]("")
- [2.4&colon; Using Rates of Change to Create a Graphical Model]("")
- [2.5&colon; Solving Problems Involving Rates of Change]("")

This summary utilizes various concepts defined in past summaries, and the *Prerequisite Modules* section so ensure you have a fully-developed understanding of everything there

## 2.1&colon; Determining Average Rate of Change

The average rate of change&mdash;abbreviated to, $$$AROC$$$&mdash;, is the average speed whereat a function changes over a specified interval of time or other independent variable.

Determining the average rate of change can be done by calculating the slope of a secant line&mdash;a secant line is simply a linear line drawn between point $$$(0,0)$$$, and point $$$(0, 0)$$$&mdash; with this formula:

@UIComponent.LaTeX({ "code": "f(x)=\\\\frac{f(x_2)-f(x_1)}{x_2-x_1}", "textAlign": "center" })

!!!NOTE

Though the *average rate of change* (*AROC*) may seem slightly similar to the *slope*, it's not; *AROC* measures overall change over an interval, while slope describes the steepness of a line.

!!!

For example, given the function $$$f(x)=6x^2-3x+5$$$ (which is graphed below), here's how you could find the average rate of change with a secant line; **assume the dependent (y-axis) variable is distance in meters, and the independent (x-axis) variable is time in seconds**

@UIComponent.Chart({ "chartID": "secant-example-i" })

Moreover, it is notable that when finding the average rate of change, you must include units

!!!NOTE

The sign of the slope of the secant line can indicate one of three things:

- if the slope is **negative**, the intervals are **decreasing**;
- if the slope is **positive**, the intervals are **increasing**;
- if the slope is **equal to zero**, **no change** occurs

!!!