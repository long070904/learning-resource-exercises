function [y,t] = nm2cm(x,t)
% NM2CM Convert signal amplitudes from nanometres to centimetres.
% Provenance: short function provided in the authenticated Academy lesson:
% https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=3v1&lesson=4&section=1
% Applied successfully to the course signals in Signal Analyzer.
% One centimetre is 10^7 nanometres; time values pass through unchanged.
y = x/1e7;
end
