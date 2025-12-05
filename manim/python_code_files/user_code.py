from cmath import rect
from manim import *
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
from sympy import nsimplify, latex, I


class DJScene(Scene):

    def construct(self):
        
        input_n = 3
        input_f = 1

        self.algorithm_steps()
        
        self.display_function(input_f)
        circuit, dashed_lines, psi_labels = self.create_circuit(n=input_n, f=input_f)

        
        
        self.show_analysis_steps(
            circuit=circuit,
            dashed_lines=dashed_lines,
            psi_labels=psi_labels,
            n=input_n,
            f=input_f
        )

        self.wait(2)


    def create_circuit(self, n=1, f=1):

        upper_qubit = r"\left|0\right\rangle^{\otimes %d}" % n
        lower_qubit = r"\left|1\right\rangle"
        

        line_y_positions = [0.8, -0.8]  # top and bottom

        Lines = VGroup()
        
        for y in line_y_positions:        
            Lines.add(Line([-5, y, 0], [6, y, 0]))

        upper_qubit_label = MathTex(upper_qubit).next_to(Lines[0].get_start(), LEFT)
        lower_qubit_label = MathTex(lower_qubit).next_to(Lines[1].get_start(), LEFT)

        # Hadamard Gates
        h_box_border = Rectangle(width=1, height=1, color=WHITE)
        h_box = Rectangle(width=1, height=1, color=BLACK, fill_opacity=1)
        h_label = MathTex("H")
        h_label.move_to(h_box.get_center())
        hadamard = VGroup(h_box, h_box_border, h_label)
        hadamard.move_to([-3, line_y_positions[1], 0])

        h_box_border = Rectangle(width=1.25, height=1, color=WHITE)
        h_box = Rectangle(width=1.25, height=1, color=BLACK, fill_opacity=1)
        h_label = MathTex(f"H^{{\\otimes {n}}}")
        h_label.move_to(h_box.get_center())
        hadamard_nbit = VGroup(h_box, h_box_border, h_label)
        hadamard_nbit.move_to([-2.9, line_y_positions[0], 0])

        hadamard_nbit_copy = hadamard_nbit.copy()
        hadamard_nbit_copy.move_to([3, line_y_positions[0], 0])

        # Oracle box
        oracle_box_border = Rectangle(width=3.5, height=4, color=WHITE)
        oracle_box = Rectangle(width=3.5, height=4, color=BLACK, fill_opacity=1)
        
        oracle_box.move_to([0, 0, 0])
        oracle_box_border.move_to([0, 0, 0])

        top_left_label = MathTex("x").scale(0.7)
        top_right_label = MathTex("x").scale(0.7)
        bottom_left_label = MathTex("y").scale(0.7)
        bottom_right_label = MathTex("y \\oplus f(x)").scale(0.7)

        top_left_label.next_to(oracle_box.get_corner(UL), DOWN*4.5 + RIGHT*0.5)
        top_right_label.next_to(oracle_box.get_corner(UR), DOWN*4.5 + LEFT*0.5)
        bottom_left_label.next_to(oracle_box.get_corner(DL), UP*4.2 + RIGHT*0.5)
        bottom_right_label.next_to(oracle_box.get_corner(DR), UP*4.2 + LEFT*0.5)

        # Dashed vertical lines marking different states
        psi_x_positions = [-4.0, -2.0, 2.0, 4.0]
        dashed_lines = VGroup()
        psi_labels = VGroup()

        top_y = line_y_positions[0] + 1
        bot_y = line_y_positions[1] - 1
        for i, x in enumerate(psi_x_positions):
            dl = DashedLine([x, top_y, 0], [x, bot_y, 0], dash_length=0.12)
            dl.set_stroke(color=WHITE, width=2)
            lbl = MathTex(r"\psi_{%d}" % i).scale(0.9)
            lbl.move_to([x, bot_y - 0.6, 0])
            dashed_lines.add(dl)
            psi_labels.add(lbl)

        # Measure box
        meter_box_border = RoundedRectangle(corner_radius=0, width=1, height=1, color=WHITE)
        meter_box = RoundedRectangle(corner_radius=0, width=1, height=1, color=BLACK, fill_opacity=1)
        arrow = Arrow(
            start=meter_box.get_bottom() + UP * 0.5, 
            end=meter_box.get_bottom() + UP * 0.9 + RIGHT * 0.3, 
            buff=0, 
            color=WHITE
        )
        arc = Arc(radius=0.35, start_angle=0, angle=TAU/2, arc_center=meter_box.get_bottom() + UP * 0.5)
        measure_symbol = VGroup(meter_box, meter_box_border, arrow, arc)
        measure_symbol.move_to(Lines[0].get_end() + LEFT * 0.35)

        # Draw wires
        self.play(Create(Lines))
        self.wait(0.5)

        # Add qubit labels
        self.play(FadeIn(upper_qubit_label), FadeIn(lower_qubit_label))
        self.wait(0.8)

        rt_initial_labels = VGroup(upper_qubit_label, lower_qubit_label)
        rt_Lines = VGroup(Lines)

        # Show hadamard gates
        self.play(FadeIn(hadamard), FadeIn(hadamard_nbit), FadeIn(hadamard_nbit_copy))
        self.wait(0.8)

        rt_hadamards = VGroup(hadamard, hadamard_nbit, hadamard_nbit_copy)

        # Reveal oracle
        self.play(FadeIn(oracle_box), FadeIn(oracle_box_border), FadeIn(top_left_label), 
                  FadeIn(top_right_label), FadeIn(bottom_left_label), FadeIn(bottom_right_label))
        self.wait(1.0)

        rt_oracle = VGroup(oracle_box, oracle_box_border, top_left_label, top_right_label, 
                          bottom_left_label, bottom_right_label)
        
        # Draw measurement symbol
        self.play(FadeIn(measure_symbol))
        self.wait(2)

        rt_measure = VGroup(measure_symbol)

        # Show all psi markers sequentially
        self.play(FadeIn(dashed_lines[0]), FadeIn(psi_labels[0]))
        self.wait(0.8)

        self.play(FadeIn(dashed_lines[1]), FadeIn(psi_labels[1]))
        self.wait(1.2)

        self.play(FadeIn(dashed_lines[2]), FadeIn(psi_labels[2]))
        self.wait(1.5)

        self.play(FadeIn(dashed_lines[3]), FadeIn(psi_labels[3]))
        self.wait(1.7)

        circuit = VGroup(
            rt_initial_labels, rt_Lines, rt_hadamards, rt_oracle, rt_measure, dashed_lines, psi_labels
        )
        self.wait(2)

        return circuit, dashed_lines, psi_labels
    

    def display_function(self, f):
        # 2 is normal 3 is inverted balanced
        # 1 is normal 4 is inverted constant
        if f == 2 or f == 3:
            balanced = True
        elif f == 1 or f == 4:
            balanced = False
            
        if balanced:
            oracle_text = MathTex("f(x) = \\text{balanced}", font_size=60)
        else:
            oracle_text = MathTex("f(x) = \\text{constant}", font_size=60)

        self.play(Write(oracle_text))
        self.wait(1)

        # Shift to top left
        self.play(oracle_text.animate.to_corner(UL, buff=0.3))
        self.wait(1)
        
        return balanced
    

    def show_analysis_steps(self, circuit, dashed_lines, psi_labels, n, f):
        """
        Shows each state step by step - alternating between circuit and analysis.
        """
        state_zero = self.compute_psi0(n)
        state_one = self.compute_psi1(n)
        state_two = self.compute_psi2(n, f)
        state_three = self.compute_psi3(n, f)

        states = [state_zero, state_one, state_two, state_three]

        for i in range(4):
            self.play(FadeIn(circuit))
            self.wait(2)
            # Highlight current psi line
            self.play(
                Indicate(dashed_lines[i], scale_factor=1.2, color=YELLOW),
                Indicate(psi_labels[i], scale_factor=1.2, color=YELLOW)
            )
            self.wait(1)

            self.play(FadeOut(circuit))
            self.wait(1)

            #Show psi label and state
            psi_label = MathTex(f"\\psi_{i}", font_size=50)
            psi_label.move_to(UP * 1.2)  # slightly above center

        
            state_text = MathTex(states[i], font_size=40)

            # Auto-resize long lines
            if state_text.width > config.frame_width - 1:
                state_text.scale_to_fit_width(config.frame_width - 1)

            state_text.move_to(ORIGIN)  # center screen

            # Stack label above state
            group = VGroup(psi_label, state_text).arrange(DOWN, buff=0.4)
            group.move_to(ORIGIN)

            self.play(FadeIn(group), run_time=1.2)
            self.wait(4)

            # Remove both
            self.play(FadeOut(group), run_time=0.8)
            self.wait(1)


        

    

    
    def compute_psi0(self, n):
        # Initial state |0...0>|1>
        state = r"|"
        for _ in range(n):
            state += r"0"
        state += r"\rangle|1\rangle"
        return state
    
    def compute_psi1(self, n):
        # After Hadamards — expanded (no summation)
        # Prefactor 1/sqrt(2^n) and the target in (|0>-|1>)/sqrt(2)
        pref = r"\frac{1}{\sqrt{2^{%d}}}" % n
        target = r"\otimes \frac{|0\rangle - |1\rangle}{\sqrt{2}}"
        terms = []
        for x in range(2**n):
            b = format(x, "0%db" % n)
            terms.append(r"|%s\rangle" % b)
        expanded = " + ".join(terms)
        state = pref + " \\bigl(" + expanded + r"\bigr) " + target
        return state

    def compute_psi2(self, n, f):
        # After Oracle — expanded (no summation)
        pref = r"\frac{1}{\sqrt{2^{%d}}}" % n
        target = r"\otimes \frac{|0\rangle - |1\rangle}{\sqrt{2}}"
        terms = []
        for x in range(2**n):
            b = format(x, "0%db" % n)
            if f == 1:
                # constant oracle: no phase flip
                terms.append(r"|%s\rangle" % b)
            elif f == 2:
                # balanced oracle: flip phase for half the states
                if x < 2**(n-1):
                    terms.append(r"|%s\rangle" % b)
                else:
                    terms.append(r"(-|%s\rangle)" % b)
            elif f == 3:
                # balanced oracle (inverted): flip phase for other half
                if x < 2**(n-1):
                    terms.append(r"(-|%s\rangle)" % b)
                else:
                    terms.append(r"|%s\rangle" % b)
            elif f == 4:
                # constant oracle: all states get phase flip
                terms.append(r"(-|%s\rangle)" % b)
            
        expanded = " + ".join(terms)
        state = pref + " \\bigl(" + expanded + r"\bigr) " + target
        return state

    def compute_psi3(self, n, f):
        # After final Hadamards — expanded (no summation)
        # The double sum simplifies to a single term: |0...0> ⊗ (|0>-|1>)/√2

        if f == 1 or f == 4:
            zeros = "0" * n
            state = r"|%s\rangle \otimes \frac{|0\rangle - |1\rangle}{\sqrt{2}}" % zeros
            return state
        else:
            state = r"\text{(some state } \neq |0\ldots 0\rangle\text{)}"
    
            return state


    def algorithm_steps(self):
        ass = VGroup(
        
            MathTex(r"\text{Algorithm Steps:}"),
        
                
            MathTex(r"\text{We initialize n qubits to } |0\rangle  \text{ and one qubit to } |1\rangle."), 
            
            
    
            MathTex(r"\text{We apply Hadamard gates to all qubits to create superposition.}"),
        
            
            MathTex(r"\text{This converts the n qubits of } |0\rangle  \text{ to } |+\rangle \text{ states and the } |1\rangle \text{ to } |-\rangle  \text{ state.}"), 
            
        
            MathTex(r"\text{We apply the oracle Uf which encodes the function } f(x)."),
            MathTex(r"\text{The oracle applies a phase flip to the states based on } f(x)."),
            MathTex(r"\text{We apply Hadamard gates again to the first n qubits.}"),
        
                
            MathTex(r"\text{Finally, we measure the first n qubits to determine if } f \text{ is constant or balanced. If we get}"),
            MathTex(r"|0\ldots0\rangle , f \text{ is constant; otherwise,} f \text{ is balanced.}"),
        )     
        

        # Stack lines vertically
        ass.arrange(DOWN, aligned_edge=LEFT, buff=0.1).scale(0.7).to_edge(LEFT)

        # Animate each line
        for i, line in enumerate(ass):
            # If it's a VGroup of multiple submobjects, animate each part
            if isinstance(line, VGroup):
                self.play(*[Write(m) for m in line.submobjects])
            else:
                self.play(Write(line))
            self.wait(0.5)

            # Pause at a specific line to show additional MathTex (example: line 5)
            if i == 5:
                eq = MathTex(
                    r"U_f \left|x\right\rangle \left|-\right\rangle = (-1)^{f(x)} \left|x\right\rangle \left|-\right\rangle"
                )
                eq.next_to(line, DOWN)
                self.play(FadeIn(eq))
                self.wait(4)
                self.play(FadeOut(eq))

        self.wait(2)
        self.play(FadeOut(ass))

        

        
        
