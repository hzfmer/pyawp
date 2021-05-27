function [ydif]=func_derivative_num(xi, yi)
if(length(xi) ~= length(yi))
    disp('size of x and y arrays not matched.')
    return
end

nx=length(xi);
for i=1:nx
    
    if(i == nx)
        ydif(i)=(yi(i)-yi(i-1))/(xi(i)-xi(i-1));
    elseif(i == 1)
        ydif(i)=(yi(i+1)-yi(i))/(xi(i+1)-xi(i));
    else
        ydif(i)=(yi(i+1)-yi(i-1))/(xi(i+1)-xi(i-1));
    end
end

end