function pileDriver_test
    % Design our spring at http://springipedia.com/extension-design-theory.asp
    %  I used 0.010" Nitinol wire for the spring.  I could purchase 0.008, 0.006, or 0.004"
    %  wire (each is $40)
    close all
    %TODO add rolling resistance.
    %Compare momentum for first 100 strikes as a function of open loop
    %driving frequency.

    steelSaturatedMag = 1.36*10^6;      % A/m  http://hyperphysics.phy-astr.gsu.edu/hbase/tables/magprop.html
    maxMRIgrad = 0.023;                 %T/m  (page 4, IJRR)
    l = 0.030;                         %m, length ball can roll (inside capsule).
    steelBearingDiamInmm = 5;           %bearing sizes available from McMaster
    r = steelBearingDiamInmm/2*0.001;   % radius in m
    massBall = 4/3*pi*r^3*8530;              %m^3* kg / (m^3), mass of bearing
    SpringRate = 50;  % N/m
    %ls = 0.0025; %m SpringRestLength
    bearingVolMag = 4/3*pi*r^3*steelSaturatedMag; %bearing volume* magnetic susceptibility

    % Diagram
    %   spring    ball           ImpactPlate
    %   [\\\\|    (_)             | >
    %    -ls 0                    l

    refine = 4;
    numContacts = 100;
    frequencies = 0.5:0.05:10;
    
    for  CoeR = [0.1,0.5, 0.9];% 0.2:0.1:0.9; %0.4; %Coefficient of restitution

    ImpactVelocities = zeros(numContacts, numel(frequencies));
    Velchange = zeros(numContacts, numel(frequencies));
    Timeforcontact = zeros(numContacts, numel(frequencies));
    totalTime = zeros(1,numel(frequencies)); %creating 1:191 matrix of zeroes
    
    tic
    for fr = 1:numel(frequencies); %no. of iterations = no. of frequency values 
        display(['frequency ',num2str(frequencies(fr)), ' [',num2str(fr),'/',num2str(numel(frequencies)),']']);
        toc
        options = odeset('Events',@events,...%'OutputFcn', @odeplot,...
        'OutputSel',1,'Refine',refine); 
        
        y0 = [0; 0]; %Initialize ODE solver with position & velocity = 0
        tstart = 0; 
        tfinal = 300;
        tout = tstart; %position [m], velocity [m/s]
        yout = y0.';
        teout = [];
        yeout = [];
        ieout = [];
        
        %figure(fr);clf;
        %set(gca,'xlim',[0 1],'ylim',[-0.2*l 1.1*l]);  %TODO: fix
        %box on
        %hold on;
        
        for i = 1:numContacts %loops for total number of contacts (100), for a given square wave i/p frequency
            % Solve until the first terminal event (impact with plate). capsuleODE
            [t,y,te,ye,ie] = ode23(@capsuleODE,[tstart tfinal],y0,options);%solves from y = 0 to y = L (impact)
            if ~ishold
                hold on
            end
            % Accumulate output for integration from y = 0 to y = L
            % (impact)
            nt = length(t);
            tout = [tout; t(2:nt)];  %#ok<*AGROW>
            yout = [yout; y(2:nt,:)];
            teout = [teout; te];    % Events at tstart are never reported.
            yeout = [yeout; ye];
            ieout = [ieout; ie];
            
            % Set the new initial conditions, with .9 attenuation. This is
            % post impact during return motion
            y0(1) = l;
            y0(2) = -CoeR*y(nt,2); %New initial velocity is -CoeR * velocity at last step before impact
            
            
            ImpactVelocities(i,fr) = y(nt,2); %stores impact velocity for 100 contacts, for each frequency, as a single column; Additional frequencies as additional columns
            Velchange(i,fr) = ImpactVelocities(i,fr) - y0(2); %stores change in velocity for each contact 
            Timeforcontact(i,fr) = teout(end); %stores cumulative time for each contact
            
            % A good guess of a valid first time step is the length of
            % the last valid time step, so use it for faster computation.
            options = odeset(options,'InitialStep',t(nt)-t(nt-refine),...
                'MaxStep',t(nt)-t(1));
            tstart = t(nt); %New start time = time at last impact
            
            if abs(y(nt,2)) < 0.01
                %zeno's paradox:  the sphere is practically stuck to the top, find next time instant where applied force is
                %negative
                tstart = ceil(2*tstart*fq)/(2*fq);
            end

%             if i >= numContacts && teout(end) > 10
%                 numContacts = numContacts+1;
%             end
        end
        
%         hl = plot(teout,yeout(:,1),'ro');
%         uistack(hl,'bottom');
%         
%         plot(tout,openLoopControl(tout)*l/3+0.5*l,'g')
%         
%         legend('impacts','ball trajectory','Location','East')
%         xlabel('time [s]');
%         ylabel('length [m]');
%         title(['Sphere trajectory and the events, frequency =',num2str(frequencies(fr)),' Hz, ', num2str(i),' Contacts']);
%         hold off
%         odeplot([],[],'done');
%         uistack(hl,'top');

        totalTime(fr) =teout(end); %Stores total time for 100 contacts for each frequency value
        
        save(['piledriver_testCR_',num2str(CoeR),'.mat'],'numContacts','frequencies',...
            'ImpactVelocities','Velchange','Timeforcontact','totalTime','steelSaturatedMag','maxMRIgrad','l',...
            'steelBearingDiamInmm','r','massBall','SpringRate','bearingVolMag','CoeR');
    end
    
    % final plots
    figure(fr + 10);clf;
    plot(frequencies, totalTime,'-o')
    xlabel('Open-loop driving frequency [Hz]');
    ylabel(['Time for ',num2str(numContacts),' contacts']);
    
    figure(fr + 11);clf;
    plot(frequencies,sum(ImpactVelocities)/numContacts,'-o')
    xlabel('Open-loop driving frequency [Hz]');
    ylabel('Average Impact Velocity');
    
    figure(fr + 12);clf;
    plot(frequencies,sum(Velchange)./totalTime,'-o') 
    xlabel('Open-loop driving frequency [Hz]');
    ylabel('momentum transfer per second [m/s2]');
    
    figure(fr + 14);clf;
    plot(frequencies,sum(ImpactVelocities)./totalTime,'-o') 
    xlabel('Open-loop driving frequency [Hz]');
    ylabel('Sum of impact velocities/total time');
    end
    
    % --------------------------------------------------------------
    function [value,isterminal,direction] = events(~,y)
        % Locate the time when height passes through zero in a
        % decreasing direction and stop integration.
        value = l-y(1);     % Detect height = 0; Stops integration when this value = 0
        isterminal = 1;   % Stop the integration
        direction = -1;   % Negative direction only; i.e. When l - y(1) is decreasing
    end
    
    %function sign = openLoopControl(t)
     %   fq = frequencies(fr);  %excitation frequency
      %  sign = -mod(floor(2*t*fq),2)*2+1; %floor(2*t*fq) can either be an even or odd integer -> mod() will respectively be 0 or 1 - > sign will be +1 or -1
    %end
    
    function dydt = capsuleODE(t,y) %ODE solver for 1 time step; Starts from y = 0 and Fb accelerates ball in +x direction initially till impact, when integration stops
        forceOnBall = bearingVolMag*maxMRIgrad;
        
        if y(2) < 0 %when velocity is less than 0 i.e. when ball is moving towards spring + during spring compression
            forceOnBall = -forceOnBall;
          
             
        end
               
        springforce = 0;
        if(y(1)<0)  %spring is only engaged when position < 0.
            springforce = -SpringRate*y(1); %negative springrate because y(1) < 0 during compression -> Net spring force is positive
        end
        
        dydt = [y(2); 1/massBall*(forceOnBall+springforce)]; %integrates and returns y(1), y(2) values from y = 0 to y = L (impact)
        
    end
    
end

%end