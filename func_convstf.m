function [tsi, ysi]=func_convstf(ti_syn, yi_syn, Tc, Td, ti_stf, yi_stf)
%ti_syn: Times of the minimum-phase synthetic waveform
%yi_syn: Amplitudes of of the minimum-phase synthetic waveform
%Tc: Characteristics time scale of the minimum-phase stf
%Td: Time shift of the minimum-phase stf
%ti_stf: Times of the new stf
%yi_stf: Amplitudes of the new stf

dt_syn=mean(diff(ti_syn));
dt_stf=mean(diff(ti_stf));
dt=min([dt_syn dt_stf]);

%New time axis
%t0=0;
t0=min([min(ti_syn) min(ti_stf)]);
t1=max([max(ti_syn) max(ti_stf)]);
Nt=round((t1-t0)/dt)+1;
ti=t0+(0:Nt-1)*dt;

%Interpolation
yi_syn_interp=interp1(ti_syn, yi_syn, ti, 'linear', 0);
yi_stf_interp=interp1(ti_stf, yi_stf, ti, 'linear', 0);


%Decon and convolution
dydt=func_derivative_num(ti, yi_stf_interp);
d2ydt2=func_derivative_num(ti, dydt);
yfil=yi_stf_interp+(2*Tc*dydt)+((Tc^2)*d2ydt2);
ytmp=conv(yi_syn_interp,yfil)*dt;
ysi=ytmp(1:Nt);
tsi=ti-(Td-t0);

% figure
% subplot(3,1,1)
% plot(ti, yi_syn_interp)
% subplot(3,1,2)
% plot(ti, yi_stf_interp)
% subplot(3,1,3)
% plot(tsi, ysi)
% hold on
% plot(ti, yi_syn_interp, 'r--')
end