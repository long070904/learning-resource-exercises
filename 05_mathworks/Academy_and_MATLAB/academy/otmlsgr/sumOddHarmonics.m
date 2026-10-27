function sumOddHarmonics(nHarmonics)
% Course-provided helper for the square-wave project in otmlsgr.
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% The actual helper source was opened and reviewed in the hosted course.
% sumOddHarmonics(10) completed there with one output.
% Saved-file adaptation: the closing end is explicit; computations are kept.
oddNums=1:2:(2*nHarmonics-1);
A=1./oddNums;
fs=3*max(oddNums);
t=(0:1/fs:3);
y=A*sin(2*pi*oddNums'*t);
plot(t,y);
title("Square wave approximation with "+nHarmonics+" terms");
end
